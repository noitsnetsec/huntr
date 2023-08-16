#theharvesterGUI.py
from tkinter import Frame, Text, Button, Entry, Label, FLAT, simpledialog, Canvas
import tkinter as tk
import random
import subprocess
import os
import threading
from tkinter import ttk
from tkinter.ttk import Scrollbar
import yaml
import sys
import urllib.parse
import platform

def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def clear_terminal(terminal):
    terminal.delete('1.0', 'end')

def ignore_input(event):
    if event.keysym == 'c' and event.state & 0x4:  # Check for Ctrl+C
        return
    return "break"

def copy_text(event, terminal, root):
    # Only copy if there's a text selection
    if terminal.selection_get():
        root.clipboard_clear()
        root.clipboard_append(terminal.selection_get())

def threaded_install(terminal):
    thread = threading.Thread(target=install_requirements, args=(terminal,))
    thread.start()

def install_requirements(terminal):
    clear_terminal(terminal)
    terminal.tag_configure("yellow", foreground="#FFFF00")
    terminal.insert('end', "======================\nINSTALLING REQUIREMENTS\n======================\n", "yellow")
    requirements_path = './Addons/TheHarvester/requirements/base.txt'
    result = subprocess.run(['pip', 'install', '-r', requirements_path], capture_output=True, text=True)
    terminal.after(0, lambda: terminal.insert('end', result.stdout + result.stderr + "\n"))
    scroll_terminal_to_end(terminal, scrollbar)


def threaded_process_input(input_data, terminal, scrollbar):
    thread = threading.Thread(target=process_input, args=(input_data, terminal, scrollbar))
    thread.start()

def process_input(input_data, terminal, scrollbar):
    # Extract the netloc (domain) from the input
    domain = urllib.parse.urlparse(input_data).netloc or input_data
    clear_terminal(terminal)
    terminal.insert('end', "========================================================================================================================\nSTARTING..\n\nPlease wait while the results are being processed.\n========================================================================================================================\n\n", "white_centered")
    
    # Get the directory where this Python file resides
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to theHarvester.py from the current directory
    harvester_path = os.path.join(current_directory, 'Addons', 'theHarvester', 'theHarvester.py')
    
    # Check the OS and decide the python command and path based on it
    os_name = platform.system()
    
    if os_name == "Windows":
        python_command = 'python'
    elif os_name == "Linux":
        python_command = 'python3'
    else:
        raise Exception(f"Unsupported operating system: {os_name}")
    
    command = [python_command, harvester_path, "-d", domain, "-l", "1000", "-b", "anubis,baidu,bevigil,bing,bingapi,bufferoverun,censys,certspotter,crtsh,dnsdumpster,duckduckgo,fullhunt,hackertarget,hunter,netlas,onyphe,otx,rapiddns,securityTrails,sitedossier,subdomaincenter,subdomainfinderc99,threatminer,tomba,urlscan,virustotal,yahoo,zoomeye", "-s"]
    
    # Construct the working directory
    working_dir = os.path.join(current_directory, 'Addons', 'theHarvester')
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir, universal_newlines=True)
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        terminal.insert('end', nextline)
        scroll_terminal_to_end(terminal, scrollbar)
    error_lines = process.stderr.readlines()
    for err_line in error_lines:
        terminal.insert('end', err_line, "red")
        scroll_terminal_to_end(terminal, scrollbar)

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("THE HARVESTER")  # Setting the text to "PING SCAN"
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

def print_instructions(terminal, scrollbar):
    instructions = """
    
    
    
=======================================================The Harvester====================================================

[Purpose]
This tool performs a thorough search on a domain to identify emails, subdomains, and more. 


It uses sources such as:

Anubis, Baidu, Bevigil, Bing, Bingapi, Bufferoverun, Censys, Certspotter, Crtsh, Dnsdumpster, Duckduckgo, Fullhunt,
Hackertarget, Hunter, Netlas, Onyphe, Otx, Rapiddns, SecurityTrails, Sitedossier, Subdomaincenter, Subdomainfinderc99,
Threatminer, Tomba, Urlscan, Virustotal, Yahoo and Zoomeye


[Instructions]
1. Enter a domain name in the box above (e.g., google.com).
2. Click the "SEARCH" button.
3. If you wish to perform another search, click the "CLEAR" button to reset the terminal.
4. To exit the tool, click the "X" button in the top right.


[Disclaimer]
Always ensure you have the legal right to perform any actions using this tool. 
Only use for ethical purposes and ensure you have proper authorization before collecting any data.

========================================================================================================================"""
    terminal.insert('end', instructions, 'white_centered')
    scroll_terminal_to_end(terminal, scrollbar)

def scroll_terminal_to_end(terminal, scrollbar):
    terminal.see(tk.END)
    terminal.configure(scrollregion=terminal.bbox(tk.END))

def save_api_keys(api_key_data):
    # Manually create YAML strings
    lines = []
    lines.append("apikeys:")
    for source, key_values in api_key_data["apikeys"].items():
        lines.append(f"  {source}:")
        for key, value in key_values.items():
            # Only add a line if the value is provided
            if value.strip():  
                lines.append(f"    {key}: {value}")
            else:
                lines.append(f"    {key}:")
        lines.append("")  # This will add a blank line between each source
    
    # Join lines to form the final YAML content
    content = '\n'.join(lines)
    
    with open('./Addons/TheHarvester/API-Keys.yaml', 'w') as outfile:
        outfile.write(content)

def api_submission_window():
    api_keys = {
        "anubis": ["key"],
        "baidu": ["key"],
        "bevigil": ["key"],
        "bing": ["key"],
        "bingapi": ["key"],
        "bufferoverun": ["key"],
        "censys": ["id", "secret"],
        "certspotter": ["key"],
        "crtsh": ["key"],
        "dnsdumpster": ["key"],
        "duckduckgo": ["key"],
        "fullhunt": ["key"],
        "hackertarget": ["key"],
        "hunter": ["key"],
        "netlas": ["key"],
        "onyphe": ["key"],
        "otx": ["key"],
        "rapiddns": ["key"],
        "securityTrails": ["key"],
        "sitedossier": ["key"],
        "subdomaincenter": ["key"],
        "subdomainfinderc99": ["key"],
        "threatminer": ["key"],
        "tomba": ["key", "secret"],
        "urlscan": ["key"],
        "virustotal": ["key"],
        "yahoo": ["key"],
        "zoomeye": ["key"],
        "shodan": ["key"],
    }

    top = tk.Toplevel(bg='gray3')  
    top.title("Enter API Keys")
    top.geometry('800x800')  

    api_key_data = {}
    entries = {}

    # Load existing API keys
    try:
        with open('./Addons/TheHarvester/API-Keys.yaml', 'r') as infile:
            existing_api_data = yaml.safe_load(infile)
            existing_api_keys = existing_api_data.get('apikeys', {})
    except FileNotFoundError:
        existing_api_keys = {}

    for idx, (source, keys) in enumerate(api_keys.items()):
        label = tk.Label(top, text=source.capitalize(), bg='gray3', fg='red')
        label.grid(row=idx, column=0, pady=0, padx=0)
        entries[source] = {}
        for j, key in enumerate(keys):
            key_entry = Entry(top, width=50, bg='gray3', fg='red')
            
            # Populate the Entry widgets with loaded values
            if existing_api_keys.get(source, {}).get(key):
                key_entry.insert(0, existing_api_keys[source][key])
                
            key_entry.grid(row=idx, column=j+1)
            entries[source][key] = key_entry

    def submit_keys():
        # Create the template dynamically based on api_keys structure
        template = {}
        for source, keys in api_keys.items():
            template[source] = {}
            for key in keys:
                template[source][key] = ""
        
        # Populate template with values from widgets
        for source, key_widgets in entries.items():
            for key, widget in key_widgets.items():
                value = widget.get()
                if value.strip():  # Check if the string is non-empty
                    template[source][key] = value
    
        # Save the updated template
        api_key_data = {"apikeys": template}
        save_api_keys(api_key_data)
        top.destroy()
    

    submit_button = Button(top, text="Submit", fg="black", bg="red", relief=FLAT, command=submit_keys)
    submit_button.grid(row=idx + 1, column=0, columnspan=2, pady=20)  # Adjust as needed


def create_theharvester_frame(master, open_frame, reconnaissance_frame, btn_font):
    theharvester_frame = Frame(master, bg='gray3')
    
    # Configure the Scrollbar's style
    style = ttk.Style()
    style.configure('TScrollbar', troughcolor='black', gripcount=0,
                    background='red', darkcolor='red', lightcolor='red', 
                    bordercolor='black', arrowcolor='red')

    # Add the new style.map() section here
    style.map('TScrollbar',
              background=[('!disabled', 'red'), ('active', 'darkred')],
              troughcolor=[('!disabled', 'black')],
              darkcolor=[('!disabled', 'red')],
              lightcolor=[('!disabled', 'red')])

    dynamic_text = DynamicTextCanvas(theharvester_frame, bg='gray3', width=800, height=60)
    dynamic_text.pack(pady=0)
    
    terminal_frame = Frame(theharvester_frame, bg='gray3')
    terminal_frame.pack(pady=10)

    domain_label = Label(terminal_frame, text="ENTER DOMAIN NAME:", bg='gray3', fg='red', font=('System', 10))
    
    domain_entry = Entry(terminal_frame, width=50, bg='gray3', fg='red')
    domain_entry.bind('<Return>', lambda event: process_input(domain_entry.get(), terminal))
    
    scan_button = Button(terminal_frame, text="SEARCH", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: threaded_process_input(domain_entry.get(), terminal, scrollbar))
    scan_button.bind("<Enter>", on_enter)
    scan_button.bind("<Leave>", on_leave)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 12, 'bold'), command=lambda: open_frame(theharvester_frame, reconnaissance_frame, "reconnaissance"))
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    api_button = Button(terminal_frame, text="Enter API Keys", fg="black", bg="red", relief=FLAT, font=('System', 10), command=api_submission_window)

    # Declare and initialize terminal first
    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.grid(row=1, column=0, columnspan=6, pady=10)

    terminal.tag_configure("white_centered", foreground="white", justify='center')
    

    scrollbar = ttk.Scrollbar(terminal_frame, orient="vertical", command=terminal.yview, style='TScrollbar')
    scrollbar.grid(row=1, column=6, sticky='nsew')
    scrollbar['style'] = 'TScrollbar'

    terminal['yscrollcommand'] = scrollbar.set

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, master))

    print_instructions(terminal, scrollbar)
    
    domain_label.grid(row=0, column=1)
    domain_entry.grid(row=0, column=2)
    scan_button.grid(row=0, column=3)
    clear_button.grid(row=0, column=4)
    back_button.grid(row=0, column=5)
    api_button.grid(row=3, column=5)

    

    return theharvester_frame