# portscan.py (port scanner file using nmap)
from tkinter import Frame, Text, Button, Entry, Label, StringVar, OptionMenu, messagebox, FLAT, filedialog
import subprocess
import threading
import webbrowser
import random
import tkinter as tk
import os
import platform

# Global variable to store the subprocess reference
proc = None

# Add the hover effect functions
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


def print_instructions(terminal):
    instructions = """



=========================================== HUNTR PORT SCANNER INSTRUCTIONS ==========================================

[Purpose]
A tool to perform port scanning on target IPs. Use ethically and with authorization.

[Procedure]

1. Enter the target IP or domain name.
2. Choose the type of scan from the dropdown.
3. Click "SCAN" to begin.
4. Monitor progress in the terminal.
5. Use the "CLEAR" button to remove the results.
6. "EXPORT SCAN" button: Save the scan results to a file.
7. "X" button: Return to the previous frame.

[Custom Scan]
   - Type the desired nmap options into the "CUSTOM NMAP OPTIONS" field.
   - Press the "RUN CUSTOM SCAN" button to execute with the given options.
   - Click on the "?" button to view the Nmap Custom Scan Options Guide for available commands.

Note: Always get proper permissions before using.

========================================================================================================================
"""
    terminal.insert('end', instructions, ('centered', 'white'))

def nmap_options_guide(terminal):
    guide = """


=========================================== NMAP CUSTOM SCAN OPTIONS GUIDE ==========================================
[A] Commonly Used Options:
    -sS: Stealth SYN Scan
    -sT: Connect Scan
    -sU: UDP Scan
    -sV: Version Detection
    -O:  OS Detection
    -F:  Fast Scan (Scan fewer ports)
    -p-: Scan all ports (1-65535)

[B] Timing and Performance:
    -T0 to -T5: Set timing template (higher is faster)
    -Pn: Treat all hosts as online (skip host discovery)

[C] Output Options:
    -oN: Normal output
    -oX: XML output
    -oG: Grepable output

[D] Discovery Options:
    -PE/PP/PM: ICMP echo, timestamp, and netmask request discovery probes
    -PS/PA/PU/PY[port list]: TCP SYN/ACK, UDP or SCTP discovery to given ports

Always refer to the official nmap documentation for a comprehensive list of options and their explanations.

========================================================================================================================
"""
    terminal.delete('1.0', 'end')
    terminal.insert('end', guide, ('centered', 'white'))

def get_nmap_path():
    system_type = platform.system()

    if system_type == "Windows":
        default_path = "C:\\Progra~2\\Nmap\\nmap.exe"
        if os.path.exists(default_path):
            return default_path
        else:
            return "nmap.exe"  # Might be in the system's PATH.
    elif system_type == "Linux":
        return "/usr/bin/nmap"
    else:
        return "nmap"  # Default, might be Mac or other UNIX-like systems. Assume nmap is in the PATH.

NMAP_PATH = get_nmap_path()

def portscan(target_ip, scan_type, terminal, scan_types, ask_redirect_download_page):
    global proc
    def run():
        terminal.delete('1.0', 'end')
        terminal.insert('end', '-'*40 + '\n')
        terminal.insert('end', f'### {scan_type} Selected ###\n')
        terminal.insert('end', '-'*40 + '\n')
        
        command_list = [NMAP_PATH] + scan_types[scan_type]['command'].replace('target_ip', target_ip).split()[1:]
        try:
            proc = subprocess.Popen(command_list, stdout=subprocess.PIPE)
            for line in iter(proc.stdout.readline, b''):
                terminal.insert('end', line)
                terminal.see('end')
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            ask_redirect_download_page('nmap')

    threading.Thread(target=run, daemon=True).start()

def custom_scan(target_ip, nmap_options, terminal):
    global proc
    def run():
        terminal.delete('1.0', 'end')
        terminal.insert('end', '-'*40 + '\n')
        terminal.insert('end', f'### Custom Scan Selected with Options: {nmap_options} ###\n')
        terminal.insert('end', '-'*40 + '\n')
        
        command_list = [NMAP_PATH] + nmap_options.split() + [target_ip]
        try:
            proc = subprocess.Popen(command_list, stdout=subprocess.PIPE)
            for line in iter(proc.stdout.readline, b''):
                terminal.insert('end', line)
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
            ask_redirect_download_page('nmap')

    threading.Thread(target=run, daemon=True).start()

def clear_terminal(terminal):
    terminal.delete('1.0', 'end')

def export_scan(terminal):
    content = terminal.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return
    with open(file_path, 'w') as file:
        file.write(content)

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("NMAP")  # Setting the text to "PING SCAN"
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

def create_portscan_frame(root, open_frame, reconnaissance_frame, button_font, ask_redirect_download_page):
    scan_types = {
        '<Select Scan>': {
            'command': NMAP_PATH + ' ',
            'description': ''
        },
        'Simple Scan': {
            'command': NMAP_PATH + ' -sn -R -v target_ip',
            'description': 'A basic scan that does not require admin privileges.'
        },
        'Stealth Scan': {
            'command': NMAP_PATH + ' -sS -v -A target_ip',
            'description': 'A stealth scan that requires admin privileges and performs OS detection, version detection, script scanning, and traceroute.'
        },
        'Extra Stealthy Scan': {
            'command': NMAP_PATH + ' -sS -v -T2 -f target_ip',
            'description': 'A slower, stealthier scan that fragments packets.'
        },
        'Version Scan': {
            'command': NMAP_PATH + ' -sV -v target_ip',
            'description': 'A scan that performs service version detection.'
        },
        'Intense Scan': {
            'command': NMAP_PATH + ' -sS -A -v -p- -T4 target_ip',
            'description': 'An intense scan that scans all ports and performs OS detection, version detection, script scanning, and traceroute.'
        }
    }

    def update_description(*args):
        description_label.config(text=scan_types[scan_type.get()]['description'])

    portscan_frame = Frame(root, bg='gray3')

    # Add the DynamicTextCanvas animation
    dynamic_text = DynamicTextCanvas(portscan_frame, bg='gray3', width=800, height=60)
    dynamic_text.pack(pady=0)  # Adds padding on the top and bottom

    terminal_frame = Frame(portscan_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    terminal_frame = Frame(portscan_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    custom_options_label = Label(terminal_frame, text="CUSTOM NMAP OPTIONS:", bg='gray3', fg='red', font=('System', 10))
    custom_options_label.grid(row=4, column=0)

    custom_options_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    custom_options_entry.grid(row=4, column=1)

    custom_scan_button = Button(terminal_frame, text="RUN CUSTOM SCAN", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: custom_scan(target_entry.get(), custom_options_entry.get(), terminal))
    custom_scan_button.bind("<Enter>", on_enter)
    custom_scan_button.bind("<Leave>", on_leave)
    custom_scan_button.grid(row=4, column=3)

    options_guide_button = Button(terminal_frame, text="?", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: nmap_options_guide(terminal))
    options_guide_button.bind("<Enter>", on_enter)
    options_guide_button.bind("<Leave>", on_leave)
    options_guide_button.grid(row=4, column=2)

    target_label = Label(terminal_frame, text="ENTER TARGET:", bg='gray3', fg='red', font=('System', 10))
    target_label.grid(row=0, column=0)

    target_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    target_entry.grid(row=0, column=1)

    scan_type = StringVar()
    scan_type.set('<Select Scan>')
    scan_type.trace('w', update_description)

    scan_optionmenu = OptionMenu(terminal_frame, scan_type, *scan_types.keys())
    scan_optionmenu.config(font=('System', 10), fg='black', bg='red')
    scan_optionmenu.grid(row=0, column=2, padx=0)

    scan_button = Button(terminal_frame, text="SCAN", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: portscan(target_entry.get(), scan_type.get(), terminal, scan_types, ask_redirect_download_page))
    scan_button.bind("<Enter>", on_enter)
    scan_button.bind("<Leave>", on_leave)
    scan_button.grid(row=0, column=3)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)
    clear_button.grid(row=0, column=4)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 10, 'bold'), command=lambda: open_frame(portscan_frame, reconnaissance_frame, "reconnaissance"), height=1, width=2)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=0, column=5)

    description_label = Label(terminal_frame, text=scan_types['<Select Scan>']['description'], bg='gray3', fg='red', font=('System', 10))
    description_label.grid(row=1, column=0, columnspan=6)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.grid(row=1, column=0, columnspan=6, pady=10)
    terminal.tag_configure('centered', justify='center')
    terminal.tag_configure('white', foreground='white')
    print_instructions(terminal)

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))

    export_button = Button(terminal_frame, text="EXPORT SCAN", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: export_scan(terminal))
    export_button.bind("<Enter>", on_enter)
    export_button.bind("<Leave>", on_leave)
    export_button.grid(row=4, column=5)

    return portscan_frame
