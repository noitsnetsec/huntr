#pingscan.py (ping scan feature file)
from tkinter import Frame, Text, Button, Entry, Label, FLAT
from tkinter import messagebox
import subprocess
import tkinter as tk
import threading
import os
import platform
import random

# Global process reference
process = None

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


def ping(target_ip, terminal, root, ask_redirect_download_page):
    def run():
        global process
        terminal.delete('1.0', 'end')
        try:
            # Determine the platform and adjust the ping command accordingly
            if platform.system() == "Windows":
                cmd = f'ping {target_ip} -n 12'
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            elif platform.system() == "Linux":
                cmd = ['/usr/bin/ping', target_ip, '-c', '12']
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            else:
                raise ValueError("Unsupported OS")

            for line in iter(process.stdout.readline, b''):
                terminal.insert('end', line)
            process = None
        except FileNotFoundError:
            ask_redirect_download_page('ping')

    threading.Thread(target=run, daemon=True).start()

def stop_process():
    global process
    if process:
        process.terminate()

def clear_terminal(terminal):
    terminal.delete('1.0', 'end')


###################################
#ANIMATION GOES HERE###############


class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("PING SCAN")  # Setting the text to "PING SCAN"
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
    

##################END OF ANIMATION#

def create_ping_frame(root, open_frame, reconnaissance_frame, button_font, ask_redirect_download_page):
    global process

    ping_frame = Frame(root, bg='gray3')
    
    # Create an instance of the DynamicTextCanvas
    dynamic_text = DynamicTextCanvas(ping_frame, bg='gray3', width=800, height=60)  # Adjust the width and height as needed
    dynamic_text.pack(pady=0)  # Adds padding on the top and bottom

    terminal_frame = Frame(ping_frame, bg='gray3')
    terminal_frame.pack(pady=0)
    target_label = Label(terminal_frame, text="ENTER TARGET:", bg='gray3', fg='red', font=('System', 10))
    target_label.grid(row=0, column=0)

    target_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    target_entry.grid(row=0, column=1)

    scan_button = Button(terminal_frame, text="SCAN", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: ping(target_entry.get(), terminal, root, ask_redirect_download_page))
    scan_button.bind("<Enter>", on_enter)
    scan_button.bind("<Leave>", on_leave)
    scan_button.grid(row=0, column=2, padx=0)

    stop_button = Button(terminal_frame, text="STOP", fg="black", bg="red", relief=FLAT, font=('System', 10), command=stop_process)
    stop_button.bind("<Enter>", on_enter)
    stop_button.bind("<Leave>", on_leave)
    stop_button.grid(row=0, column=3)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)
    clear_button.grid(row=0, column=4)

    def on_exit():
        dynamic_text.stop_animation()

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 10, 'bold'), height=1, width=2)
    back_button['command'] = lambda: [on_exit(), open_frame(ping_frame, reconnaissance_frame, "reconnaissance")]
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=0, column=5)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.grid(row=1, column=0, columnspan=6, pady=10)

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))


    return ping_frame
