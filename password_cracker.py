from tkinter import Frame, Text, Button, Entry, Label, filedialog, StringVar, OptionMenu, FLAT
import hashlib
import threading
import os
import random
import tkinter as tk
import subprocess
import sys

stop_cracking = False

def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def center_ascii_art(art, terminal_width):
    centered_art = ""
    for line in art.split('\n'):
        padding = (terminal_width - len(line)) // 2
        centered_line = ' ' * padding + line + '\n'
        centered_art += centered_line
    return centered_art

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
    terminal_width = 120  # Define the terminal width here
    
    separator = "=======================================================================================================================\n"

    # ASCII art for the header
    ascii_art = """
.s    s.  .s5SSSs.  .s5SSSs.  .s    s.      .s5SSSs.  .s5SSSs.  .s5SSSs.  .s5SSSs.  .s    s.  .s5SSSs.  .s5SSSs.  
      SS.       SS.       SS.       SS.           SS.       SS.       SS.       SS.       SS.       SS.       SS. 
sS    S%S sS    S%S sS    `:; sS    S%S     sS    `:; sS    S%S sS    S%S sS    `:; sS    S%S sS    `:; sS    S%S 
SS    S%S SS    S%S SS        SS    S%S     SS        SS    S%S SS    S%S SS        SS    S%S SS        SS    S%S 
SSSs. S%S SSSs. S%S `:;;;;.   SSSs. S%S     SS        SS .sS;:' SSSs. S%S SS        SSSSs.S:' SSSs.     SS .sS;:' 
SS    S%S SS    S%S       ;;. SS    S%S     SS        SS    ;,  SS    S%S SS        SS  "SS.  SS        SS    ;,  
SS    `:; SS    `:;       `:; SS    `:;     SS        SS    `:; SS    `:; SS        SS    `:; SS        SS    `:; 
SS    ;,. SS    ;,. .,;   ;,. SS    ;,.     SS    ;,. SS    ;,. SS    ;,. SS    ;,. SS    ;,. SS    ;,. SS    ;,. 
:;    ;:' :;    ;:' `:;;;;;:' :;    ;:'     `:;;;;;:' `:    ;:' :;    ;:' `:;;;;;:' :;    ;:' `:;;;;;:' `:    ;:' \n
"""
    
    centered_art = center_ascii_art(ascii_art, terminal_width)

    # Individual components for better color control
    title_prefix = "========================================== "
    title_main = "HUNTR HASH CRACKER INSTRUCTIONS"
    title_suffix = " ============================================\n\n"

    purpose_header = "[Purpose]\n"
    purpose_body = "- This tool is designed to crack hashes by performing a brute force attack using a wordlist. \n- It supports MD5, SHA1, SHA256, and SHA512 hash algorithms. \n- Ensure you have the legal right to crack the hash.\n\n"
    procedure_header = "[Procedure]"
    procedure_body = """
1.) Enter Hash: Input the hash you wish to crack.
2.) Hash Type: Choose the hash algorithm used to generate the hash.
3.) Load Wordlist: Load the wordlist that will be used to attempt to crack the hash.
4.) Crack: Start the cracking process.
5.) Stop: Stop the cracking process.
6.) Clear: Clear the terminal's content.
"""
    security_note = "\n\n\nOnly use this tool for ethical and legal purposes. Always have proper authorization before attempting to crack any hash.\n"
    
    # Insert parts with appropriate coloring and alignment
    terminal.insert('end', separator, 'red')  # Inserting separator above the ASCII art
    terminal.insert('end', centered_art, 'white')  # Centered ASCII art
    terminal.insert('end', title_prefix, 'red')
    terminal.insert('end', title_main, 'white')
    terminal.insert('end', title_suffix, 'red')
    terminal.insert('end', purpose_header, 'white')
    terminal.insert('end', purpose_body, 'red')
    terminal.insert('end', procedure_header, 'white')
    terminal.insert('end', procedure_body, 'red')
    terminal.insert('end', security_note, 'white')
    terminal.insert('end', separator, 'red')  # Inserting separator at the end



class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("HASH CRACKER")  # Setting the text to "PING SCAN"
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

def play_sound(sound_file):
    """Plays a sound based on the operating system."""
    if os.name == 'posix':  # Linux, Unix, etc.
        os.system(f'paplay {sound_file}')
    elif os.name == 'nt':  # Windows
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def crack_password(hash_type, hash_entry, terminal, wordlist):
    def run():
        global stop_cracking
        stop_cracking = False
        terminal.delete('1.0', 'end')
        try:
            with open(wordlist, 'r', errors='ignore') as file:
                for i, line in enumerate(file.readlines(), 1):
                    if stop_cracking:
                        terminal.insert('end', 'Cracking process stopped.\n')
                        terminal.see('end')
                        break
                    word = line.rstrip()
                    hash_word = hashlib.new(hash_type, word.encode()).hexdigest()

                    terminal.insert('end', f'Attempt {i}: {word}\n')
                    terminal.see('end')
                    if hash_word == hash_entry:
                        terminal.insert('end', '\n[+] Password Found: ', 'yellow')
                        terminal.insert('end', f'{word}\n', 'yellow_bold')
                        terminal.see('end')
                        play_sound(os.path.join('media', 'sounds', 'pass_cracked_sfx.wav'))
                        break
                else:
                    terminal.insert('end', 'Password not found in wordlist.\n')
                    terminal.see('end')
        except FileNotFoundError:
            terminal.insert('end', 'Wordlist file not found.\n')
            terminal.see('end')

    threading.Thread(target=run, daemon=True).start()

def stop_password_cracking():
    global stop_cracking
    stop_cracking = True

def clear_terminal(terminal):
    terminal.delete('1.0', 'end')


def create_password_cracker_frame(root, open_frame, offensive_frame, button_font):

    password_cracker_frame = Frame(root, bg='gray3')

    # Create an instance of the DynamicTextCanvas
    dynamic_text = DynamicTextCanvas(password_cracker_frame, bg='gray3', width=800, height=60)  # Adjust the width and height as needed
    dynamic_text.pack(pady=0)  # Adds padding on the top and bottom

    terminal_frame = Frame(password_cracker_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    terminal_frame = Frame(password_cracker_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    hash_label = Label(terminal_frame, text="ENTER HASH:", bg='gray3', fg='red', font=('System', 10))
    hash_label.grid(row=0, column=0)

    hash_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    hash_entry.grid(row=0, column=1)

    hash_type = StringVar(terminal_frame)
    hash_type.set("MD5")
    hash_type_menu = OptionMenu(terminal_frame, hash_type, "MD5", "SHA1", "SHA256", "SHA512")
    hash_type_menu.config(bg='red', fg='black', font=('System', 10), relief=FLAT, highlightbackground='red', highlightthickness=1, bd=0)
    hash_type_menu.grid(row=0, column=2)

    wordlist_button = Button(terminal_frame, text="LOAD WORDLIST", relief=FLAT, fg="black", bg="red", font=('System', 10))
    wordlist_button.grid(row=0, column=3)
    wordlist_button.bind("<Enter>", on_enter)
    wordlist_button.bind("<Leave>", on_leave)

    def load_wordlist():
        wordlist = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        wordlist_button['text'] = wordlist if wordlist else "LOAD WORDLIST"

    wordlist_button.config(command=load_wordlist)

    crack_button = Button(terminal_frame, text="CRACK", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: crack_password(hash_type.get(), hash_entry.get(), terminal, wordlist_button['text']))
    crack_button.grid(row=0, column=4)
    crack_button.bind("<Enter>", on_enter)
    crack_button.bind("<Leave>", on_leave)

    stop_button = Button(terminal_frame, text="STOP", fg="black", bg="red", relief=FLAT, font=('System', 10), command=stop_password_cracking)
    stop_button.grid(row=0, column=5)
    stop_button.bind("<Enter>", on_enter)
    stop_button.bind("<Leave>", on_leave)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.grid(row=0, column=6)
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 12, 'bold'), command=lambda: open_frame(password_cracker_frame, offensive_frame, "offensive"), height=1, width=2)
    back_button.grid(row=0, column=7)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.tag_configure('white_centered', foreground='white', justify='center')
    terminal.tag_config('yellow', foreground='yellow')
    terminal.tag_config('yellow_bold', foreground='yellow', font=('System', 10, 'bold'))
    terminal.grid(row=1, column=0, columnspan=8, pady=10)

    # Define the tags
    terminal.tag_configure('white', foreground='white')
    terminal.tag_configure('red', foreground='red')
    terminal.tag_configure('centered', justify='center')  # Define centered tag

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))

    print_instructions(terminal)


    return password_cracker_frame
