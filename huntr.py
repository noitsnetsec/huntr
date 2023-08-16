#huntr.py (main file)
import time
import threading
import random
import atexit

def type_print(text, type_delay=0.004, end_delay=0.35):
    """Simulates typing by printing text one character at a time."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(type_delay)
    print()  # Newline after finishing typing
    time.sleep(end_delay)

def random_colored_ascii(ascii_art):
    """Returns ASCII art with characters randomly colored."""
    result = ""
    for char in ascii_art:
        if char != ' ' and char != '\n':
            # Three white for every red to make white more frequent
            color_code = random.choice(['\033[97m', '\033[97m', '\033[97m', '\033[97m', '\033[97m', '\033[91m'])  
            result += color_code + char
        else:
            result += char
    return result + '\033[0m'  # Reset color at the end


def typing_animation():
    # ASCII Art for "STARTING HUNTR"
    huntr_ascii = """
 .S    S.   .S       S.   .S_sSSs   sdSS_SSSSSSbs  .S_sSSs    
.SS    SS. .SS       SS. .SS~YS%%b  YSSS~S%SSSSSP .SS~YS%%b   
S%S    S%S S%S       S%S S%S   `S%b      S%S      S%S   `S%b  
S%S    S%S S%S       S%S S%S    S%S      S%S      S%S    S%S  
S%S SSSS%S S&S       S&S S%S    S&S      S&S      S%S    d*S  
S&S  SSS&S S&S       S&S S&S    S&S      S&S      S&S   .S*S  
S&S    S&S S&S       S&S S&S    S&S      S&S      S&S_sdSSS   
S&S    S&S S&S       S&S S&S    S&S      S&S      S&S~YSY%b   
S*S    S*S S*b       d*S S*S    S*S      S*S      S*S   `S%b  
S*S    S*S S*S.     .S*S S*S    S*S      S*S      S*S    S%S  
S*S    S*S  SSSbs_sdSSS  S*S    S*S      S*S      S*S    S&S  
SSS    S*S   YSSP~YSSY   S*S    SSS      S*S      S*S    SSS  
       SP                SP              SP       SP          
       Y                 Y               Y        Y           
    """
    print(random_colored_ascii(huntr_ascii))
    animated_lines = [
        "\033[93m[+]\033[0m Analyzing Signatures...",
        "\033[93m[+]\033[0m Verifying Integrity...",
        "\033[93m[+]\033[0m Establishing Connections...",
        "\033[93m[+]\033[0m Preparing Environments...",
        "\033[92m[SUCCESS]\033[0m ",
    ]

    for line in animated_lines:
        type_print(line)

def on_exit():
    """Function to be executed on exit."""
    print("\033[91m[STOPPED]\033[0m")

# Register the function to be called on exit
atexit.register(on_exit)

# Start the animation in a separate thread.
animation_thread = threading.Thread(target=typing_animation)
animation_thread.start()

#IMPORTS
from tkinter import Tk, Frame, Button, Label, font, BOTTOM, CENTER, messagebox, FLAT, Toplevel, Checkbutton, IntVar, Text
from PIL import Image, ImageTk
from webbrowser import open_new
import pingscan
import portscan
import vulnscan
from vulnscan import create_vulnscan_frame
import info_gathering
from info_gathering import create_info_gathering_frame
import password_cracker
from password_cracker import create_password_cracker_frame
from hash_identifier import create_hash_identifier_frame
import resources
from resources import create_resources_frame
import tkinter as tk
import dirbuster
from dirbuster import create_dirbuster_frame
import sys
import bruteforce
from bruteforce import create_tool_frame
import theharvesterGUI
from theharvesterGUI import create_theharvester_frame
import psutil
import requests
import subprocess
import os
import requests
import ctypes
import metasploit
from metasploit import create_metasploit_frame
import signal
import platform
import configparser
import set as set_module
from set import create_set_frame

global logo
logo = None
tor_process = None
IS_WINDOWS = platform.system() == "Windows"
config = configparser.ConfigParser()
config.read('settings.ini')

#########################
def show_startup_message():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    show_message = config.getboolean('Preferences', 'show_startup_message')
    
    if not show_message:
        return

    response = messagebox.askyesno(
        "NOTICE",
        "Would you like to view the README.txt file?\n\n"
        "- Highly recommended before using tool as I am a beginner "
        "\n\nYou can turn off this popup in the options menu by pressing:\n ~ or `"
    )
    if response:  # If the user selects 'Yes'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        readme_path = os.path.join(current_dir, "README.txt")
        if IS_WINDOWS:
            os.system(f"notepad {readme_path}")
        else:
            os.system(f"xdg-open {readme_path}")


#########################

if IS_WINDOWS:
    import winreg as reg

def get_current_proxy_settings():
    if IS_WINDOWS:
        key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        hKey = reg.OpenKey(reg.HKEY_CURRENT_USER, key)
        
        # Default values if not present
        proxy_enable = 0
        proxy_server = ""
        try:
            proxy_enable, reg_type = reg.QueryValueEx(hKey, "ProxyEnable")
            proxy_server, reg_type = reg.QueryValueEx(hKey, "ProxyServer")
        except:
            pass  # If there's an exception, the key might not exist, so use the default values.
        reg.CloseKey(hKey)
        
        return proxy_enable, proxy_server
    else:  # Linux, assuming GNOME desktop for simplicity
        proxy_mode = os.popen("gsettings get org.gnome.system.proxy mode").read().strip()
        socks_host = os.popen("gsettings get org.gnome.system.proxy.socks host").read().strip()
        socks_port = os.popen("gsettings get org.gnome.system.proxy.socks port").read().strip()
        
        return proxy_mode, (socks_host, socks_port)

# This function will be called before we modify the registry to start the Tor service.
# It will save the current proxy settings so we can restore them later.
original_proxy_enable, original_proxy_server = get_current_proxy_settings()


def reset_proxy_settings():
    if IS_WINDOWS:
        key = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        hKey = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
        
        reg.SetValueEx(hKey, "ProxyEnable", 0, reg.REG_DWORD, original_proxy_enable)
        reg.SetValueEx(hKey, "ProxyServer", 0, reg.REG_SZ, original_proxy_server)
        
        reg.CloseKey(hKey)
    else:  # Linux, assuming GNOME desktop for simplicity
        os.system("gsettings set org.gnome.system.proxy mode 'none'")

def set_system_proxy(enable, address="127.0.0.1", port=9050):
    if IS_WINDOWS:
        path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        hKey = reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_ALL_ACCESS)
        
        # Enable proxy
        reg.SetValueEx(hKey, "ProxyEnable", 0, reg.REG_DWORD, 1 if enable else 0)
        
        # Set SOCKS proxy settings
        if enable:
            proxy_string = f"socks={address}:{port}"
            reg.SetValueEx(hKey, "ProxyServer", 0, reg.REG_SZ, proxy_string)
        
        reg.CloseKey(hKey)
    else:  # Linux, assuming GNOME desktop for simplicity
        if enable:
            os.system(f"gsettings set org.gnome.system.proxy mode 'manual'")
            os.system(f"gsettings set org.gnome.system.proxy.socks host '{address}'")
            os.system(f"gsettings set org.gnome.system.proxy.socks port '{port}'")
        else:
            os.system("gsettings set org.gnome.system.proxy mode 'none'")



def check_tor_process():
    tor_process_name = 'tor.exe' if IS_WINDOWS else 'tor'
    for process in psutil.process_iter():
        try:
            if process.name().lower() == tor_process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def check_tor_connectivity():
    """
    Returns True if able to connect through Tor, otherwise returns False.
    """
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    try:
        response = requests.get('https://check.torproject.org/', proxies=proxies, timeout=10)
        
        # If the response contains "Congratulations", it means Tor is working
        if "Congratulations" in response.text:
            return True
        return False
    except requests.RequestException:
        return False

def check_tor_status():
    tor_process_status = check_tor_process()
    tor_connectivity_status = check_tor_connectivity()

    if tor_process_status and tor_connectivity_status:
        messagebox.showinfo("Tor Status", "Tor is running and connectivity is working.")
    elif tor_process_status:
        messagebox.showwarning("Tor Status", "Tor process is running but connectivity isn't working. Check your settings.")
    else:
        messagebox.showerror("Tor Status", "Tor is not running.")

def threaded_check_tor_status():
    thread = threading.Thread(target=check_tor_status)
    thread.start()

def read_output(process, terminal_text):
    """Utility function to read the output from the TOR process and print it to the terminal text widget."""
    while True:
        output = process.stdout.readline()
        if output:
            terminal_text.insert(tk.END, output)
            terminal_text.see(tk.END)
        else:
            break

def validate_tor_started(process, terminal_text):
    """
    Validate that the Tor process has started correctly and update the terminal text widget.
    """
    # Check if the Tor process is still running after it's been started
    if process.poll() is None:
        terminal_text.insert(tk.END, "Tor has started successfully.\n")
        
        # Set the system-wide proxy settings to use Tor
        set_system_proxy(True)
    else:
        terminal_text.insert(tk.END, "There was an issue starting Tor. Please check the logs above.\n")

def start_tor(root, terminal_text):
    """
    Start the TOR process and configure system proxy settings to use TOR.
    """
    global tor_process

    if tor_process:
        terminal_text.insert(tk.END, "Tor is already running.\n")
        return

    # Check if Tor is already running as a separate process outside of our application
    if check_tor_process():
        terminal_text.insert(tk.END, "Tor is already running outside this application. Please stop it and try again.\n")
        return

    # If we reach here, Tor is not already running, so we can start it
    if IS_WINDOWS:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        tor_path = os.path.join(current_dir, "Addons", "TOR", "tor", "tor.exe")
    else:  # Linux or other Unix-like systems
        tor_path = "tor"

    try:
        process = subprocess.Popen(tor_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        tor_process = process

        # Start a new thread to read the output of the process
        threading.Thread(target=read_output, args=(process, terminal_text)).start()

        # After 5 seconds, check if the Tor process is still running (it should be if everything is okay)
        root.after(5000, lambda: validate_tor_started(process, terminal_text))

    except Exception as e:
        terminal_text.insert(tk.END, f"Failed to start Tor: {e}\n")



def stop_tor(terminal_text):
    """
    Stop the TOR process and reset system proxy settings.
    """
    global tor_process

    if not tor_process:
        terminal_text.insert(tk.END, "Tor is not running.\n")
        return

    try:
        if IS_WINDOWS:
            os.system('taskkill /f /im tor.exe')
        else:  # Linux or other Unix-like systems
            os.kill(tor_process.pid, signal.SIGTERM)
            tor_process.wait()

        # Reset proxy settings to their original state
        reset_proxy_settings()

        tor_process = None
        terminal_text.insert(tk.END, "Tor has been stopped.\n")

    except Exception as e:
        terminal_text.insert(tk.END, f"Failed to stop Tor: {e}\n")


def open_options_window():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    options_win = Toplevel(root)
    options_win.title("Huntr Options Menu")
    options_win.geometry('600x600')  # Size of 600x600
    options_win.configure(bg='gray3')  # Background color

    # Check if the configuration setting is 'yes' or 'true'
    startup_msg_value = config.get('Preferences', 'show_startup_message').lower()
    if startup_msg_value in ['yes', 'true']:
        startup_msg_var_value = 1
    else:
        startup_msg_var_value = 0

    startup_msg_var = IntVar(value=startup_msg_var_value)
    
    startup_msg_check = Checkbutton(options_win, text="Show Startup Message", variable=startup_msg_var, bg='gray3', fg='red', activebackground='gray3', activeforeground='red')
    startup_msg_check.pack(pady=10)
    
    # Text widget for terminal output
    terminal_text = Text(options_win, width=70, height=15, bg='gray3', fg='red')  # Text color updated
    terminal_text.pack(pady=10)

    # Start and Stop Tor buttons
    start_tor_button = Button(options_win, text="Start TOR", command=lambda: start_tor(options_win, terminal_text), bg='gray3', fg='red', activebackground='gray3', activeforeground='red')  # Text color updated and command updated
    start_tor_button.pack(pady=(0,5))
    
    stop_tor_button = Button(options_win, text="Stop TOR", command=lambda: stop_tor(terminal_text), bg='gray3', fg='red', activebackground='gray3', activeforeground='red')
    stop_tor_button.pack(pady=(0,5))
    
    # Check Tor Status Button
    check_tor_status_button = Button(options_win, text="Check TOR Status", command=threaded_check_tor_status, bg='gray3', fg='red', activebackground='gray3', activeforeground='red')
    check_tor_status_button.pack(pady=(0,20))

    # Close button for the options window
    close_button = Button(options_win, text="Close", command=options_win.destroy, bg='gray3', fg='red', activebackground='gray3', activeforeground='red')  # Text color updated
    close_button.pack(pady=20)

    def save_settings():
        config['Preferences']['show_startup_message'] = str(startup_msg_var.get())
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    save_button = Button(options_win, text="Save Settings", command=save_settings, bg='gray3', fg='red', activebackground='gray3', activeforeground='red')
    save_button.pack(pady=20)
    

    options_win.mainloop()

def go_back_to_main_frame(event=None):
    open_frame(reconnaissance_frame, main_frame, "huntr")  # replace this line with your back button's function logic


#######################################################################
# Top Animation 

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        # New Phrases
        self.phrases = ["SECURITY TESTING TOOL", "RECONNAISSANCE", "FORENSICS", "OFFENSIVE", "DEFENSIVE", "DIRECTORY BUSTING", "HASH CRACKING", "PORT SCANNING"]
        self.current_phrase_index = 0
        self.text_values = list(self.phrases[self.current_phrase_index])
        self.after_ids_text = []
        self.after_ids_box = []
        self.raining_chars = []
        self.bind("<Map>", self.start_animation)
        self.after_id_switch = None

    def reset_state(self):
        # Stop any ongoing animations.
        self.stop_animation()
    
        # If a phrase switch is scheduled, cancel it.
        if self.after_id_switch:
            self.after_cancel(self.after_id_switch)
            self.after_id_switch = None
        
        # Clear the canvas.
        self.delete("all")
        
        # Reinitialize the variables.
        self.text_positions = []
        self.after_ids_text = []
        self.after_ids_box = []
        self.raining_chars = []
        self.flashed_chars = set()

    def restart_animation(self):
        self.reset_state()  # Reset canvas and all variables.
        self.start_animation()  # Start the animation again.

    def start_animation(self, event=None):
        char_width, char_height = self.font_size(self.font)
        spacing = 1
        self.unbind("<Map>")
        total_chars_width = sum([self.font_size(self.font, char=char)[0] for char in self.text_values])
        total_spacing_width = spacing * (len(self.text_values) - 1)
        total_width = total_chars_width - total_spacing_width
    
        x = (self.winfo_width() - total_width) / 2
        y = 10  # small padding from the top
    
        for i, char in enumerate(self.text_values):
            individual_char_width = self.font_size(self.font, char=char)[0]
            position = self.create_text(x, y, text=char, font=self.font, fill="#080808", anchor=tk.NW)
            self.text_positions.append(position)
            x += individual_char_width - spacing
            
        self.flashed_chars = set()
        self.flash_next_char()
        
        # Schedule switch_phrase here
        self.after_id_switch = self.after(7000, self.switch_phrase)
    
    def switch_phrase(self):
        if self.after_id_switch:
            self.after_cancel(self.after_id_switch)
            self.after_id_switch = None
                
        self.current_phrase_index += 1
        if self.current_phrase_index >= len(self.phrases):
            self.current_phrase_index = 0
        self.text_values = list(self.phrases[self.current_phrase_index])
            
        # Call reset_state here before starting a new animation
        self.reset_state()
        self.start_animation()
            
        # Schedule switch_phrase here only
        self.after_id_switch = self.after(7000, self.switch_phrase)
    

    def flash_next_char(self):
        if len(self.flashed_chars) < len(self.text_positions):
            random_char_index = random.choice([i for i in range(len(self.text_positions)) if i not in self.flashed_chars])
            self.flashed_chars.add(random_char_index)
            current_char = self.text_positions[random_char_index]
            self.delete(f"swipe_rect_{random_char_index}")
            self.itemconfig(current_char, fill="red")
            x_coord, y_coord = self.coords(current_char)
            raining_char_position = self.create_text(x_coord, y_coord + 10, text=self.itemcget(current_char, 'text'), font=self.font, fill="red", anchor=tk.W)
            self.raining_chars.append((raining_char_position, 0))
            self.after(70, self.flash_next_char)
        else:
            self.update_animation()
    

    def change_single_character(self, char_position):
        self.itemconfig(char_position, text=random.choice(self.chars))
        self.after_ids_text.append(self.after(50, self.change_single_character, char_position))

    def update_animation(self):
        for i, position in enumerate(self.text_positions):
            char = self.itemcget(position, 'text')
            if random.random() < 0.002:
                raining_char_position = self.create_text(self.coords(position)[0], self.coords(position)[1], text=char, font=self.font, fill="red", anchor=tk.W)
                self.raining_chars.append((raining_char_position, 0))
        to_remove = []
        for rain, step in self.raining_chars:
            if self.exists(rain):  # Add this check
                x, y = self.coords(rain)
                fade_color = self.get_fading_color(step)
                if fade_color == "#080808":  # This is our last color
                    to_remove.append((rain, step))
                    continue
                self.itemconfig(rain, fill=fade_color)
                if y < self.winfo_height():
                    self.move(rain, 0, 1)
                    self.raining_chars[self.raining_chars.index((rain, step))] = (rain, step + 1)
                else:
                    to_remove.append((rain, step))
        for rain, step in to_remove:
            self.raining_chars.remove((rain, step))
            self.delete(rain)
        after_id = self.after(10, self.update_animation)
        self.after_ids_box.append(after_id)
    
    def exists(self, item):
        """Check if a canvas item exists."""
        return item in self.find_all()
    

    def font_size(self, font, char="Test"):
        test = tk.Label(self, text=char, font=font)
        width = test.winfo_reqwidth()
        height = test.winfo_reqheight()
        test.destroy()
        return width, height

    def stop_animation(self):
        for after_id in self.after_ids_text:
            self.after_cancel(after_id)
        for after_id in self.after_ids_box:
            self.after_cancel(after_id)
        self.after_ids_text.clear()
        self.after_ids_box.clear()
    

    def get_fading_color(self, step):
        shades = [
            "#ff0000", "#fa0000", "#f50000", "#f00000", "#eb0000", 
            "#e60000", "#e10000", "#dc0000", "#d70000", "#d20000", 
            "#cd0000", "#c80000", "#c30000", "#be0000", "#b90000", 
            "#b40000", "#af0000", "#aa0000", "#a50000", "#a00000", 
            "#9b0000", "#960000", "#910000", "#8c0000", "#870000", 
            "#820000", "#7d0000", "#780000", "#730000", "#6e0000", 
            "#690000", "#640000", "#5f0000", "#5a0000", "#550000", 
            "#500000", "#4b0000", "#460000", "#410000", "#3c0000", 
            "#370000", "#320000", "#2d0000", "#280000", "#230000", 
            "#1e0000", "#190000", "#140000", "#0f0000", "#0a0000",
            "#080808"
        ]
        return shades[min(step, len(shades)-1)]

# end of
#######################################################################
#######################################################################
# Bottom Animation

class BottomDynamicTextCanvas(DynamicTextCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.font = ('Consolas', 9)
        self.text_values = ["A", "9", "2", "M", "D", "2", "K", "Z", "H", "T", "Q", "L", "X", "3", "Y", "P", "E", "G", "B", "R", "U", "O", "C", "F", "I", "V", "4"] + [random.choice(self.chars) for _ in range(90)]
        # Add this line to bind the resize event
        self.bind("<Configure>", self.handle_resize)
        self.start_animation()  # Start the animation right away

    def handle_resize(self, event):
        self.restart_animation()

    def start_animation(self, event=None):
        char_width, char_height = self.font_size(self.font)
        spacing = 30
        self.unbind("<Map>")
        total_chars_width = sum([self.font_size(self.font, char=char)[0] for char in self.text_values])
        total_spacing_width = spacing * (len(self.text_values) - 2)
        total_width = total_chars_width - total_spacing_width
    
        x = (self.winfo_width() - total_width) / 2
        y = self.winfo_height() - char_height + 15
    
        for i, char in enumerate(self.text_values):
            individual_char_width = self.font_size(self.font, char=char)[0]
            position = self.create_text(x, y, text=char, font=self.font, fill="red", anchor=tk.W)
            x += individual_char_width - spacing
            self.text_positions.append(position)
            self.change_single_character(position)  # Start changing each character right away
    
        self.update_animation()

    def flash_next_char(self):
        if len(self.flashed_chars) < len(self.text_positions):
            random_char_index = random.choice([i for i in range(len(self.text_positions)) if i not in self.flashed_chars])
            self.flashed_chars.add(random_char_index)
            current_char = self.text_positions[random_char_index]
            self.itemconfig(current_char, fill="red")
            self.change_single_character(current_char)  # Ensure this method is called
            self.after(100, self.flash_next_char)
        else:
            self.update_animation()
    

    def change_single_character(self, char_position):
        self.itemconfig(char_position, text=random.choice(self.chars))
        self.after_ids_text.append(self.after(350, self.change_single_character, char_position))

    def update_animation(self):
        for i, position in enumerate(self.text_positions):
            char = self.itemcget(position, 'text')
            if random.random() < 0.001:
                raining_char_position = self.create_text(self.coords(position)[0], self.coords(position)[1], text=char, font=self.font, fill="red", anchor=tk.W)
                self.raining_chars.append((raining_char_position, 0))
        to_remove = []
        for rain, step in self.raining_chars:
            x, y = self.coords(rain)
            fade_color = self.get_fading_color(step)
            if fade_color == "#080808":  # This is our last color
                to_remove.append((rain, step))
                continue
            self.itemconfig(rain, fill=fade_color)
            if y > 0:  # Change here to make sure characters don't go past the top of the canvas
                self.move(rain, 0, -5)  # Change the y motion to negative to make it go upwards
                self.raining_chars[self.raining_chars.index((rain, step))] = (rain, step + 2)
    
            else:
                to_remove.append((rain, step))
        for rain, step in to_remove:
            self.raining_chars.remove((rain, step))
            self.delete(rain)
        after_id = self.after(15, self.update_animation)
        self.after_ids_box.append(after_id)

    def font_size(self, font, char="Test"):
        test = tk.Label(self, text=char, font=font)
        width = test.winfo_reqwidth()
        height = test.winfo_reqheight()
        test.destroy()
        return width, height

    def stop_animation(self):
        for after_id in self.after_ids_text:
            self.after_cancel(after_id)
        for after_id in self.after_ids_box:
            self.after_cancel(after_id)
        self.after_ids_text.clear()
        self.after_ids_box.clear()

    def get_fading_color(self, step):
        shades = [
            "#ff0000", "#fa0000", "#f50000", "#f00000", "#eb0000", 
            "#e60000", "#e10000", "#dc0000", "#d70000", "#d20000", 
            "#cd0000", "#c80000", "#c30000", "#be0000", "#b90000", 
            "#b40000", "#af0000", "#aa0000", "#a50000", "#a00000", 
            "#9b0000", "#960000", "#910000", "#8c0000", "#870000", 
            "#820000", "#7d0000", "#780000", "#730000", "#6e0000", 
            "#690000", "#640000", "#5f0000", "#5a0000", "#550000", 
            "#500000", "#4b0000", "#460000", "#410000", "#3c0000", 
            "#370000", "#320000", "#2d0000", "#280000", "#230000", 
            "#1e0000", "#190000", "#140000", "#0f0000", "#0a0000",
            "#080808"
        ]
        return shades[min(step, len(shades)-1)]

# End Of 
#######################################################################

def start_move(event):
    global root
    root.x = root.winfo_pointerx() - root.winfo_rootx()
    root.y = root.winfo_pointery() - root.winfo_rooty()

def stop_move(event):
    global root
    root.x = None
    root.y = None

def do_move(event):
    global root
    dx = root.winfo_pointerx() - root.x
    dy = root.winfo_pointery() - root.y
    root.geometry("+%s+%s" % (dx, dy))
    
def open_frame(current_frame, new_frame, title_text):
    if current_frame == main_frame:
        dynamic_text_canvas.stop_animation()
    current_frame.pack_forget()
    new_frame.pack(expand=True)
    if new_frame == main_frame:
        dynamic_text_canvas.restart_animation()  # Restart the animation for the main frame.



def ask_redirect_download_page(dependency):
    if messagebox.askyesno('Dependency not found', f'The dependency {dependency} was not found. Do you want to be redirected to the download page?'):
        if dependency == 'nmap':
            open_new('https://nmap.org/download.html')
        elif dependency == 'nslookup' or dependency == 'dig' or dependency == 'whois':
            open_new('https://www.example.com')  # replace with correct URL

# Button hover functions
def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


root = Tk()
root.geometry('1280x850')
icon = tk.PhotoImage(file='huntr_icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)
root.configure(bg='gray3')
root.title("huntr (Alpha)")
root.overrideredirect(0) # switch back to native title bar
root.bind('<F5>', lambda event=None: restart_program())


show_startup_message()  # Display the message right after initializing the root

# Loading Screen
loading_frame = Frame(root, bg='gray3')
loading_frame.pack(expand=True)

image = Image.open("huntr_logo_v2.png")  
image = image.resize((192, 108))  
logo = ImageTk.PhotoImage(image)
logo_label = Label(loading_frame, image=logo, bg='gray3')
logo_label.pack(pady=20)  

tagline = Label(loading_frame, text="All-in-One Security Testing Tool", bg='gray3', fg='red', font=('System', 12))
tagline.pack()

canvas = tk.Canvas(loading_frame, width=600, height=5, bg='gray3', highlightthickness=0)
canvas.pack(pady=10)
loading_bar = canvas.create_rectangle(0, 0, 0, 5, fill='red')

author = Label(loading_frame, text="Written by: Andre Hunt", bg='gray3', fg='white', font=('System', 9))
author.pack(side=BOTTOM, pady=10)

root.update()

# loading bar updates
for i in range(0, 601, 5):
    canvas.coords(loading_bar, 0, 0, i, 5)
    root.update()
    time.sleep(random.uniform(0.00001, 0.009))  # generates a random delay between 0.001 to 0.01 seconds

time.sleep(0.3)

loading_frame.pack_forget()

BOTTOM_CANVAS_HEIGHT = 100
BOTTOM_CANVAS_WIDTH = 3000  # Or any other width you find suitable

button_font = font.Font(family="System", size=14)  

main_frame = Frame(root, bg='gray3')
main_frame.pack(expand=True, fill=tk.BOTH)

# Create the bottom canvas right after main_frame
bottom_dynamic_text_canvas = BottomDynamicTextCanvas(main_frame, bg='gray3', width=BOTTOM_CANVAS_WIDTH, height=BOTTOM_CANVAS_HEIGHT)
bottom_dynamic_text_canvas.pack(side=tk.BOTTOM, fill=tk.X)

spacer_frame = Frame(main_frame, bg='gray3', height=30)  # Adjust height as desired for more or less spacing.
spacer_frame.pack(fill='x')

image = Image.open("huntr_logo.png")  
image = image.resize((480, 270))
logo = ImageTk.PhotoImage(image)
logo_label = Label(main_frame, image=logo, bg='gray3')
logo_label.pack(pady=45)

reconnaissance_frame = Frame(root, bg='gray3')
ping_frame = pingscan.create_ping_frame(root, open_frame, reconnaissance_frame, button_font, ask_redirect_download_page)
portscan_frame = portscan.create_portscan_frame(root, open_frame, reconnaissance_frame, button_font, ask_redirect_download_page)
vulnscan_frame = vulnscan.create_vulnscan_frame(root, open_frame, reconnaissance_frame, button_font, ask_redirect_download_page)
info_gathering_frame = info_gathering.create_info_gathering_frame(root, open_frame, reconnaissance_frame, button_font)

forensic_frame = Frame(root, bg='gray3')
hash_identifier_frame = create_hash_identifier_frame(root, open_frame, forensic_frame, button_font)

offensive_frame = Frame(root, bg='gray3')
password_cracker_frame = create_password_cracker_frame(root, open_frame, offensive_frame, button_font)
recon_ng_frame = create_set_frame(root, open_frame, reconnaissance_frame, button_font)

resources_frame = create_resources_frame(root, open_frame, main_frame, button_font)

# Four main buttons
recon_button = Button(main_frame, text="RECONNAISSANCE", command=lambda: open_frame(main_frame, reconnaissance_frame, "reconnaissance"), fg="black", bg="red", font=button_font, height=1, width=20, relief=FLAT)
recon_button.pack(pady=(10, 5))
recon_button.bind("<Enter>", on_enter)
recon_button.bind("<Leave>", on_leave)


forensic_button = Button(main_frame, text="FORENSIC", command=lambda: open_frame(main_frame, forensic_frame, "FORENSIC"), fg="black", bg="red", font=button_font, height=1, width=20, relief=FLAT)
forensic_button.pack(pady=5)
forensic_button.bind("<Enter>", on_enter)
forensic_button.bind("<Leave>", on_leave)

offensive_button = Button(main_frame, text="OFFENSIVE", command=lambda: open_frame(main_frame, offensive_frame, "OFFENSIVE"), fg="black", bg="red", font=button_font, height=1, width=20, relief=FLAT)
offensive_button.pack(pady=5)
offensive_button.bind("<Enter>", on_enter)
offensive_button.bind("<Leave>", on_leave)

resources_button = Button(main_frame, text="RESOURCES", command=lambda: open_frame(main_frame, resources_frame, "Resources"), fg="black", bg="red", font=button_font, height=1, width=20, relief=FLAT)
resources_button.pack(pady=5)
resources_button.bind("<Enter>", on_enter)
resources_button.bind("<Leave>", on_leave)

spacer_frame = Frame(main_frame, bg='gray3', height=60)  # Adjust height as desired for more or less spacing.
spacer_frame.pack(fill='x')


dynamic_text_canvas = DynamicTextCanvas(main_frame, bg='gray3', width=500, height=root.winfo_height() * 0.33)
dynamic_text_canvas.pack(pady=0)


# dynamic_text_canvas.start_animation()  # Remove this line to avoid calling start_animation twice


#Button(main_frame, text="X", command=root.destroy, fg="black", bg="red", font=button_font, height=1, width=2, relief=FLAT).pack(pady=80)

back_button_font = font.Font(family="System", size=12)

# For the buttons in reconnaissance_frame
ping_scan_button = Button(reconnaissance_frame, text="PING SCAN", command=lambda: open_frame(reconnaissance_frame, ping_frame, "reconnaissance/pingscan"), fg="black", bg="red", font=button_font, relief=FLAT)
ping_scan_button.bind("<Enter>", on_enter)
ping_scan_button.bind("<Leave>", on_leave)
ping_scan_button.pack(pady=5)

port_scan_button = Button(reconnaissance_frame, text="NMAP", command=lambda: open_frame(reconnaissance_frame, portscan_frame, "reconnaissance/portscan"), fg="black", bg="red", font=button_font, relief=FLAT)
port_scan_button.bind("<Enter>", on_enter)
port_scan_button.bind("<Leave>", on_leave)
port_scan_button.pack(pady=5)

vuln_scan_button = Button(reconnaissance_frame, text="EMAIL SCAN", command=lambda: open_frame(reconnaissance_frame, vulnscan_frame, "reconnaissance/vulnscan"), fg="black", bg="red", font=button_font, relief=FLAT)
vuln_scan_button.bind("<Enter>", on_enter)
vuln_scan_button.bind("<Leave>", on_leave)
vuln_scan_button.pack(pady=5)

harvester_button = Button(reconnaissance_frame, text="HARVESTR", command=lambda: open_frame(reconnaissance_frame, create_theharvester_frame(root, open_frame, reconnaissance_frame, button_font), "reconnaissance/theharvester"), fg="black", bg="red", font=button_font, relief=FLAT)
harvester_button.bind("<Enter>", on_enter)
harvester_button.bind("<Leave>", on_leave)
harvester_button.pack(pady=5)

# Button for RECON-NG in the recon menu
recon_ng_button = Button(reconnaissance_frame, text="RECON-NG", fg="black", bg="red", relief=FLAT, font=button_font, command=lambda: open_frame(reconnaissance_frame, recon_ng_frame, "recon"))
recon_ng_button.pack(pady=5, padx=20)
recon_ng_button.bind("<Enter>", on_enter)
recon_ng_button.bind("<Leave>", on_leave)

info_gathering_button = Button(reconnaissance_frame, text="WHOIS+", command=lambda: open_frame(reconnaissance_frame, info_gathering_frame, "reconnaissance/info_gathering"), fg="black", bg="red", font=button_font, relief=FLAT)
info_gathering_button.bind("<Enter>", on_enter)
info_gathering_button.bind("<Leave>", on_leave)
info_gathering_button.pack(pady=5)


# Back buttons with hover effect
recon_back_button = Button(reconnaissance_frame, text="X", command=lambda: open_frame(reconnaissance_frame, main_frame, "huntr"), fg="black", bg="red", font=back_button_font, height=1, width=2, relief=FLAT)
recon_back_button.bind("<Enter>", on_enter)
recon_back_button.bind("<Leave>", on_leave)
recon_back_button.pack(side=BOTTOM, anchor="center", padx=5, pady=20)

forensic_back_button = Button(forensic_frame, text="X", command=lambda: open_frame(forensic_frame, main_frame, "huntr"), fg="black", bg="red", font=back_button_font, height=1, width=2, relief=FLAT)
forensic_back_button.bind("<Enter>", on_enter)
forensic_back_button.bind("<Leave>", on_leave)
forensic_back_button.pack(side=BOTTOM, anchor="center", padx=5, pady=20)

offensive_back_button = Button(offensive_frame, text="X", command=lambda: open_frame(offensive_frame, main_frame, "huntr"), fg="black", bg="red", font=back_button_font, height=1, width=2, relief=FLAT)
offensive_back_button.bind("<Enter>", on_enter)
offensive_back_button.bind("<Leave>", on_leave)
offensive_back_button.pack(side=BOTTOM, anchor="center", padx=5, pady=20)

dirbuster_frame = create_dirbuster_frame(root, open_frame, reconnaissance_frame, button_font)

dirbuster_button = Button(reconnaissance_frame, text="DIRBUSTR", command=lambda: open_frame(reconnaissance_frame, dirbuster_frame, "reconnaissance/dirbuster"), fg="black", bg="red", font=button_font, relief=FLAT)
dirbuster_button.bind("<Enter>", on_enter)
dirbuster_button.bind("<Leave>", on_leave)
dirbuster_button.pack(pady=5)


# For the buttons in forensic_frame
hash_id_button = Button(forensic_frame, text="HASH IDENTIFIER", command=lambda: open_frame(forensic_frame, hash_identifier_frame, "forensic/hash_identifier"), fg="black", bg="red", font=button_font, relief=FLAT)
hash_id_button.bind("<Enter>", on_enter)
hash_id_button.bind("<Leave>", on_leave)
hash_id_button.pack(pady=80)

# For the buttons in offensive_frame
hash_cracker_button = Button(offensive_frame, text="HASH CRACKER", command=lambda: open_frame(offensive_frame, password_cracker_frame, "offensive/hash_cracker"), fg="black", bg="red", font=button_font, relief=FLAT)
hash_cracker_button.bind("<Enter>", on_enter)
hash_cracker_button.bind("<Leave>", on_leave)
hash_cracker_button.pack(pady=5)

metasploit_frame = create_metasploit_frame(root, open_frame, offensive_frame, button_font, ask_redirect_download_page)

metasploit_button = Button(offensive_frame, text="GOPHISH", fg="black", bg="red", relief=FLAT, font=button_font, command=lambda: open_frame(offensive_frame, metasploit_frame, "offensive/metasploit"))
metasploit_button.pack(pady=5, padx=20)
metasploit_button.bind("<Enter>", on_enter)
metasploit_button.bind("<Leave>", on_leave)

tool_frame = create_tool_frame(root, open_frame, offensive_frame, button_font)

tool_button = Button(offensive_frame, text="BRUTE FORCE", fg="black", bg="red", relief=FLAT, font=button_font, command=lambda: open_frame(offensive_frame, tool_frame, "tool"))
tool_button.pack(pady=5, padx=20)
tool_button.bind("<Enter>", on_enter)
tool_button.bind("<Leave>", on_leave)

root.bind("`", lambda event: open_options_window())
root.bind("~", lambda event: open_options_window())
root.mainloop()