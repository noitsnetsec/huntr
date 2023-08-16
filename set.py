#set.py (Recon-ng Feature)
from tkinter import Frame, Text, Button, Entry, Label, FLAT, ttk, simpledialog, filedialog, BOTTOM
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
    e.widget['foreground'] = 'gray3'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'gray3'

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
        self.text_values = list("RECON-NG")  # Setting the text to "PING SCAN"
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

# Utility function to calculate the padding needed to center the text
def calculate_center_padding(total_width, text_length, char_width=1):
    padding = (total_width - (text_length * char_width)) // 2
    return " " * padding

def display_recon_banner(terminal):
    terminal_width = 120
    terminal.insert('end', "=" * 120 + "\n", 'red_text')
    
    # Adding ASCII art
    terminal.insert('end', '''
                 :::::::::  :::::::::: ::::::::   ::::::::  ::::    :::            ::::    :::  :::::::: 
                :+:    :+: :+:       :+:    :+: :+:    :+: :+:+:   :+:            :+:+:   :+: :+:    :+: 
               +:+    +:+ +:+       +:+        +:+    +:+ :+:+:+  +:+            :+:+:+  +:+ +:+         
              +#++:++#:  +#++:++#  +#+        +#+    +:+ +#+ +:+ +#+  +:++#++   +#+ +:+ +#+ :#:          
             +#+    +#+ +#+       +#+        +#+    +#+ +#+  +#+#+#            +#+  +#+#+# +#+   +#+#    
            #+#    #+# #+#       #+#    :+: #+#    #+# #+#   #+#+#            #+#   #+#+# #+#    #+#     
           ###    ### ########## ########   ########  ###    ####            ###    ####  ########
\n''', 'white_text')
    
        # Centering "RECON-NG INSTRUCTIONS" within the "=" boundary
    terminal_width = 120
    instruction_text = "RECON-NG INSTRUCTIONS"
    padding_left = (terminal_width - len(instruction_text)) // 2
    terminal.insert('end', "=" * padding_left, 'red_text')
    terminal.insert('end', instruction_text, 'white_text')
    terminal.insert('end', "=" * (terminal_width - len(instruction_text) - padding_left) + "\n", 'red_text')

    # Adding some newlines to move the text down
    terminal.insert('end', "\n", 'white_text')

    # Adding prominent "CHECK README FOR INSTALL GUIDE" - Centered and with specific styling
    terminal_width = 120
    readme_text = "CHECK README FOR INSTALL GUIDE"
    padding_left = (terminal_width - len(readme_text)) // 2
    terminal.insert('end', " " * padding_left, 'white_text')  # Adding left padding
    terminal.insert('end', readme_text, 'install_guide')  # Displaying the centered text with special styling
    terminal.insert('end', "\n", 'white_text')  # New lines after the centered text

    
    # Adding [PURPOSE]
    terminal.insert('end', "\n[PURPOSE]\n", 'white_text')
    terminal.insert('end', "Recon-ng is a full-featured web reconnaissance framework written in Python. It offers an efficient environment for conducting open source intelligence (OSINT) web-based footprinting quickly and thoroughly.\n\n")

    # Features of Recon-ng
    terminal.insert('end', "[KEY FEATURES]\n", 'white_text')
    terminal.insert('end', "- Modular architecture: Easy-to-write modules and simple implementation.\n")
    terminal.insert('end', "- Interactive workspace: Tracks and organizes discovered information.\n")
    terminal.insert('end', "- Reporting: Generates detailed reports from findings.\n")
    terminal.insert('end', "- Scripting: Recon-ng can be scripted for automation, enhancing the recon process.\n")
    terminal.insert('end', "- Integration: Designed to work seamlessly with other reconnaissance and penetration testing tools.\n\n")

    # Command instructions
    terminal.insert('end', "[COMMANDS]\n", 'white_text')
    terminal.insert('end', 'start ', 'boldwhite_text')
    terminal.insert('end', "> start Recon-ng.\n")
    terminal.insert('end', 'exit ', 'boldwhite_text')
    terminal.insert('end', "> in the Ubuntu terminal to shutdown recon-ng.\n\n")

    # Adding the reminder for users
    terminal.insert('end', "\nAlways ensure you have proper authorization before conducting reconnaissance against any target.\n", 'white_text')
    terminal.insert('end', "=" * 120 + "\n", 'red_text')

def start_set(terminal): 
    if os.name == "nt":  # Check if the OS is Windows
        command = 'cmd.exe /c start wsl python3 /home/ubuntu/recon-ng/recon-ng'
        subprocess.Popen(command, shell=True)
    else:  # Assume Linux or similar Unix-like system
        command = 'x-terminal-emulator -e recon-ng'
        subprocess.Popen(command, shell=True)

def execute_command(command, terminal, command_entry):
    """Process user commands and display results in the terminal."""
    global process

    if command == "help":
        terminal.insert(tk.END, "Available commands: help, clear, exit, start, stop, reset\n")
        
    elif command == "clear":
        terminal.delete(1.0, tk.END)
        
    elif command == "exit" or command == "stop":
        terminal.insert(tk.END, "Stopping SET...\n")
        # Additional functionality to stop SET can be added here
        #...

    elif command == "start":
        terminal.insert(tk.END, "Starting SET...\n")
        start_set(terminal)  
        
    elif command == "reset":
        terminal.insert(tk.END, "Resetting...\n")
        # Additional functionality for reset can be added here
        #...
        
    else:
        terminal.insert(tk.END, f"Unrecognized command: {command}\n")
        
    terminal.see(tk.END)
    command_entry.delete(0, tk.END)  # Clear the command entry

def clear_terminal_content():
    global terminal
    terminal.delete(1.0, tk.END)

def create_set_frame(root, open_frame, parent_frame, font):
    global process

    set_frame = Frame(root, bg='gray3')
    
    dynamic_text = DynamicTextCanvas(set_frame, bg='gray3', width=800, height=60)
    dynamic_text.grid(row=1, column=0, columnspan=2)
    
    terminal_frame = Frame(set_frame, bg='gray3')
    terminal_frame.grid(row=2, column=0, columnspan=2, pady=10)

    command_entry = Entry(terminal_frame, width=48, bg='gray3', fg='red', font=('System', 18))
    command_entry.grid(row=4, column=0, columnspan=1)
    command_entry.focus_set()  
    
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

    back_button = Button(set_frame, text="X", command=lambda: open_frame(set_frame, parent_frame, "offensive"), bg='red', font=font)
    #back_button.pack(side=BOTTOM, anchor="center", padx=5, pady=20)
    back_button.grid(row=4, column=5, sticky="ne")
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)

    terminal.grid(row=1, column=0, columnspan=6, pady=10)
    terminal.tag_configure('white_text', foreground='white')
    terminal.tag_configure('red_text', foreground='red')
    terminal.tag_configure('boldwhite_text', foreground='white', font=('System', 10, 'bold'))
    terminal.tag_configure('install_guide', foreground='black', background='red', font=('System', 15, 'bold'))

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))
    # Call the function to display the banner
    display_recon_banner(terminal)
    
    command_entry.bind('<Return>', lambda e: execute_command(command_entry.get(), terminal, command_entry))
    
    return set_frame