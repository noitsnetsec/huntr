#metasploit_tool.py (Social Engineering toolkit feature file)
#metasploit_tool.py (Social Engineering toolkit feature file)
from tkinter import Frame, Text, Button, Entry, Label, FLAT, ttk, simpledialog, filedialog
from tkinter import messagebox
import subprocess
import tkinter as tk
import threading
import random
import os
import re
import signal
import sys

# Global variables
process = None

def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def clear_terminal(terminal):
    terminal.delete(1.0, tk.END)

def ignore_input(event):
    if event.keysym == 'c' and event.state & 0x4:  # Check for Ctrl+C
        return
    return "break"

def copy_text(event, terminal, root):
    # Only copy if there's a text selection
    if terminal.selection_get():
        root.clipboard_clear()
        root.clipboard_append(terminal.selection_get())

###################

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("GoPhish")  # Setting the text to "PING SCAN"
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
        print("Restarting animation...") # Debugging print
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
        y = 0  # small padding from the top
    
        for i, char in enumerate(self.text_values):
            individual_char_width = self.font_size(self.font, char=char)[0]
            position = self.create_text(x, y, text=char, font=self.font, fill="#080808", anchor=tk.NW)
            self.text_positions.append(position)
            x += individual_char_width - spacing
            
        self.flashed_chars = set()
        self.flash_next_char()
    
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
            if random.random() < 0.09:  # Adjust this value to control the frequency
                raining_char_position = self.create_text(self.coords(position)[0], self.coords(position)[1] + 10, text=char, font=self.font, fill="red", anchor=tk.W)
                self.raining_chars.append((raining_char_position, 0))
        
        to_remove = []
        
        for rain, step in self.raining_chars:
            if self.exists(rain): 
                x, y = self.coords(rain)
                fade_color = self.get_fading_color(step)
                if fade_color == "#080808":  
                    to_remove.append((rain, step))
                    continue
                self.itemconfig(rain, fill=fade_color)
                if y < self.winfo_height():  # Make sure the character remains within canvas height
                    self.move(rain, 0, 1)
                    self.raining_chars[self.raining_chars.index((rain, step))] = (rain, step + 2)  # Increase the step by 2 instead of 1 for faster fading
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
            "#ff0000", "#f50000", "#eb0000", "#e10000", 
            "#d70000", "#cd0000", "#c30000", "#b90000", 
            "#af0000", "#a50000", "#9b0000", "#910000",
            "#870000", "#7d0000", "#730000", "#690000",
            "#5f0000", "#550000", "#4b0000", "#410000",
            "#370000", "#2d0000", "#230000", "#190000",
            "#0f0000", "#080808"
        ]
        return shades[min(step, len(shades)-1)]

##################

def display_start_message(terminal):
    """Display the GoPhish started message in the terminal."""
    message_lines = [
        "-------------------------------------------------------------------------------------------------------",
        "GoPhish Status:",  # Note: Breaking this message to color 'Started' in lime green
        "",  # This line will be in lime green
        "Started",
        "",
        "- Head to the GoPhish admin server to operate.",
        "- It's recommended to review the GoPhish documentation or further your understanding through research.",
        "-------------------------------------------------------------------------------------------------------"
    ]
    
    for line in message_lines:
        if line == "Started":
            terminal.insert(tk.END, line, "limegreen_text")
        else:
            terminal.insert(tk.END, line, "white_text")
        terminal.insert(tk.END, "\n")
    terminal.see(tk.END)

def display_stop_message(terminal):
    """Display the GoPhish stopped message in the terminal."""
    message_lines = [
        "-------------------------------------------------------------------------------------------------------",
        "GoPhish Status:",
        "",
        "Stopped",  # This line will be in bold bright red
        "-------------------------------------------------------------------------------------------------------"
    ]
    
    for line in message_lines:
        if line == "Stopped":
            terminal.insert(tk.END, line, "boldred_text")
        else:
            terminal.insert(tk.END, line, "white_text")
        terminal.insert(tk.END, "\n")
    terminal.see(tk.END)

def start_gophish(terminal):  # Add terminal as a parameter
    global process

    # Check OS and set the GoPhish path accordingly
    if os.name == 'posix':
        script_directory = os.path.dirname(os.path.abspath(__file__))
        gophish_path = os.path.join(script_directory, "Addons", "GoPhish", "gophish")
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        gophish_path = os.path.join(script_directory, "Addons", "GoPhish", "gophish.exe")

    gophish_directory = "Addons/GoPhish"
    process = subprocess.Popen([gophish_path], shell=True, cwd=gophish_directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1)

    monitor_output(process, terminal)  # Pass terminal to monitor_output
FONT_SIZE = 10  # You can adjust this value as needed


def insert_colored_text(terminal, line):
    """Parse the line and insert it into the terminal with appropriate colors."""

    # Remove the undesired pattern from the start of the line and the trailing double quote
    line = re.sub(r'^time="[^"]+" level=\w+ msg="(.*?)"$', r'\1', line)

    remaining_line = line

    # Find and color URLs
    urls = re.findall(r'http://\S+|https://\S+', line)
    for url in urls:
        before, _, remaining_line = remaining_line.partition(url)
        terminal.insert(tk.END, before, "red_text")
        terminal.insert(tk.END, url, "white_text")

    # The remaining portion of the line that's not a URL is inserted in red
    terminal.insert(tk.END, remaining_line, "red_text")



def monitor_output(process, terminal):
    """Monitor GoPhish output and display it in the terminal."""
    def thread_target(terminal):
        for line in iter(process.stdout.readline, ''):
            insert_colored_text(terminal, line)
            terminal.see(tk.END)
        process.stdout.close()
    threading.Thread(target=thread_target, args=(terminal,), daemon=True).start()

def kill_gophish_linux():
    try:
        pids = subprocess.check_output(['pgrep', '-f', 'gophish']).decode('utf-8').splitlines()
        for pid in pids:
            os.kill(int(pid), signal.SIGKILL)
        return True
    except Exception as e:
        print(f"Error killing gophish: {e}")
    return False

def execute_command(command, terminal, command_entry):
    """Process user commands and display results in the terminal."""
    global process

    if command == "help":
        terminal.insert(tk.END, "Available commands: help, clear, exit, start, stop, reset\n")
        
    elif command == "clear":
        terminal.delete(1.0, tk.END)
        
    elif command == "exit" or command == "stop":
        terminal.insert(tk.END, "Stopping GoPhish...\n")
        if process:
            if sys.platform == "win32":
                try:
                    # Using taskkill to forcefully terminate gophish.exe
                    subprocess.run(["taskkill", "/F", "/T", "/IM", "gophish.exe"], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    terminal.insert(tk.END, f"Failed to stop GoPhish: {e.output}\n")
                process = None
            else:
                if not kill_gophish_linux():
                    terminal.insert(tk.END, "Failed to stop GoPhish. Please check manually.\n")
                process = None

        terminal.after(2000, lambda: display_stop_message(terminal))  # Display the stop message after 2 seconds


    elif command == "start":
        terminal.insert(tk.END, "Starting GoPhish...\n")
        start_gophish(terminal)  # Pass terminal to start_gophish
        terminal.after(2000, lambda: display_start_message(terminal))  # Display the start message after 2 seconds
        
    elif command == "reset":
        terminal.insert(tk.END, "Resetting...\n")
        if process:
            process.terminate()  # terminate the GoPhish process
            process = None
        with open('tmp/output.txt', 'w') as file:  # Clear the content of the output.txt file
            file.write('')
        terminal.insert(tk.END, "GoPhish stopped and output cleared.\n")
        
    else:
        terminal.insert(tk.END, f"Unrecognized command: {command}\n")
        
    terminal.see(tk.END)
    command_entry.delete(0, tk.END)  # Clear the command entry


def on_closing():
    if process:
        process.terminate()
    with open('tmp/output.txt', 'w') as file:  # Clear the content of the output.txt file
        file.write('')
    root.destroy()


def display_banner(terminal):
    # Define the boundary and title for consistency
    boundary = "=" * 136
    title = " HUNTR PHISHING TOOLKIT "
    
    # Adding the hash boundary
    terminal.insert('end', boundary + "\n", 'red_text')
    
    # Adding ASCII art
    terminal.insert('end', '''
                           ▄██████▄   ▄██████▄     ▄███████▄    ▄█    █▄     ▄█     ▄████████    ▄█    █▄    
                          ███    ███ ███    ███   ███    ███   ███    ███   ███    ███    ███   ███    ███   
                          ███    █▀  ███    ███   ███    ███   ███    ███   ███▌   ███    █▀    ███    ███   
                         ▄███        ███    ███   ███    ███  ▄███▄▄▄▄███▄▄ ███▌   ███         ▄███▄▄▄▄███▄▄ 
                        ▀▀███ ████▄  ███    ███ ▀█████████▀  ▀▀███▀▀▀▀███▀  ███▌ ▀███████████ ▀▀███▀▀▀▀███▀  
                          ███    ███ ███    ███   ███          ███    ███   ███           ███   ███    ███   
                          ███    ███ ███    ███   ███          ███    ███   ███     ▄█    ███   ███    ███   
                          ████████▀   ▀██████▀   ▄████▀        ███    █▀    █▀    ▄████████▀    ███    █▀      \n
''', 'white_text')
    
    # Adding the hash boundary again with title in white and boundary in red
    terminal.insert('end', boundary[:int((136-len(title))/2)], 'red_text')
    terminal.insert('end', title, 'white_text')
    terminal.insert('end', boundary[int((136+len(title))/2):] + "\n", 'red_text')
    
    # Adding [PURPOSE]
    terminal.insert('end', "\n[PURPOSE]\n", 'white_text')
    terminal.insert('end', "This toolkit is designed to facilitate ethical phishing campaigns for security awareness, testing, and training.\n\n")

    # Adding [KEY FEATURES]
    terminal.insert('end', "[KEY FEATURES]\n", 'white_text')
    terminal.insert('end', '''
- SMTP Integration: Send phishing emails via your SMTP servers.
- Campaign Management: Design and oversee phishing campaigns.
- Template Design: Craft phishing emails and landing pages.
- Content Cloning: Clone known websites and emails for realistic content.
- Landing Pages & Redirects: Capture interactions or redirect post-engagement.
- Real-Time Monitoring: Instant feedback with metrics and insights.
''')

    # Adding [BASIC COMMANDS]
    terminal.insert('end', "\n[BASIC COMMANDS]\n", 'white_text')

    # Inserting the commands and descriptions with specific words colored yellow
    terminal.insert('end', "1. ", 'red_text')
    terminal.insert('end', "start", 'white_text')
    terminal.insert('end', "  > Initiate GoPhish.\n")

    terminal.insert('end', "2. ", 'red_text')
    terminal.insert('end', "stop", 'white_text')
    terminal.insert('end', "  > Halt GoPhish.\n")

    terminal.insert('end', "3. ", 'red_text')
    terminal.insert('end', "clear", 'white_text')
    terminal.insert('end', "  > Clear terminal content.\n")

    terminal.insert('end', "4. ", 'red_text')
    terminal.insert('end', "help", 'white_text')
    terminal.insert('end', "  > View available commands and their descriptions.\n\n")


    # Adding the reminder
    terminal.insert('end', "Only use GoPhish ethically, responsibly, and with the explicit consent of all involved parties.\n", 'white_text')
    terminal.insert('end', boundary, 'red_text')

def clear_terminal_content():
    global terminal
    terminal.delete(1.0, tk.END)

def create_metasploit_frame(root, open_frame, security_frame, button_font, ask_redirect_download_page):
    global process

    metasploit_frame = Frame(root, bg='gray3')
    
    dynamic_text = DynamicTextCanvas(metasploit_frame, bg='gray3', width=800, height=60)
    dynamic_text.pack(pady=0)
    
    terminal_frame = Frame(metasploit_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    command_entry = Entry(terminal_frame, width=48, bg='gray3', fg='red', font=('System', 18))
    command_entry.grid(row=4, column=0, columnspan=1)
    command_entry.focus_set()  # Set focus to the command_entry
    
    # Added code to set a flashing cursor (similar to a terminal)
    command_entry.config(insertbackground='red', insertwidth=3)

    execute_button = Button(terminal_frame, text="EXECUTE", fg="black", bg="red", relief=FLAT, font=('System', 10), 
                                command=lambda: execute_command(command_entry.get(), terminal, command_entry))
    execute_button.bind("<Enter>", on_enter)
    execute_button.bind("<Leave>", on_leave)
    execute_button.grid(row=4, column=3, padx=10)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)
    clear_button.grid(row=4, column=4)

    def on_exit():
        dynamic_text.stop_animation()

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 10, 'bold'), height=1, width=2)
    back_button['command'] = lambda: [on_exit(), open_frame(metasploit_frame, security_frame, "security")]
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=4, column=5)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)


    terminal.grid(row=1, column=0, columnspan=6, pady=10)
    
    # Configure the tags for terminal text colors
    terminal.tag_config("white_text", foreground="white", font=("Consolas", FONT_SIZE))
    terminal.tag_config("red_text", foreground="red", font=("Consolas", FONT_SIZE))
    terminal.tag_config("limegreen_text", foreground="#32CD32", font=("Consolas", FONT_SIZE))
    terminal.tag_config("boldred_text", foreground="red", font=("Consolas", FONT_SIZE, "bold"))
    terminal.tag_config('yellow_text', foreground='yellow')
    terminal.tag_config('red_text', foreground='red')
    terminal.tag_config("boldwhite_text", foreground="white", font=("Terminal", FONT_SIZE, "bold"))
    display_banner(terminal)

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))
    
    command_entry.bind('<Return>', lambda e: execute_command(command_entry.get(), terminal, command_entry))
    
    return metasploit_frame