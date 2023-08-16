from tkinter import Frame, Text, Button, Entry, filedialog, FLAT, Label, StringVar, ttk, IntVar, Checkbutton, Toplevel
import os
import requests
import threading
import random
import time
from tkinter.ttk import Progressbar, Style
import random
import tkinter as tk
import platform

# Global flags and variables
stop_dirbusting = False
found_items = []
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
]

def auto_scroll(terminal):
    terminal.see(tk.END)

def ignore_input(event):
    if event.keysym == 'c' and event.state & 0x4:  # Check for Ctrl+C
        return
    return "break"

def copy_text(event, terminal, root):
    # Only copy if there's a text selection
    if terminal.selection_get():
        root.clipboard_clear()
        root.clipboard_append(terminal.selection_get())

######

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("DIRECTORY BUSTR")  # Setting the text to "PING SCAN"
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

#####

def on_wordlist_selection(event, combobox):
    selected = combobox.get()
    if selected == "Use custom wordlist":
        custom_wordlist = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if custom_wordlist:
            combobox.set(custom_wordlist)
        else:
            combobox.set(default_wordlist)

def clear_terminal(terminal):
    terminal.delete(1.0, tk.END)

def play_sound(sound_file):
    """Plays a sound based on the operating system."""
    if os.name == 'posix':  # Linux, Unix, etc.
        os.system(f'paplay {sound_file}')
    elif os.name == 'nt':  # Windows
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def dirbust(target, wordlist, terminal, use_agent_rotation, use_random_delay, use_recursive_scanning, use_extensions_var, progress, tooltip=None):
    clear_terminal(terminal)  # Clear the terminal when directory busting starts

    global stop_dirbusting, found_items

    extensions = ["php", "html", "js", "txt"] if use_extensions_var.get() == 1 else []

    stop_dirbusting = False
    found_items = []
    headers = {}

    terminal.insert('end', "-------------------------------\n")
    terminal.insert('end', "Starting Huntr Directory Buster\n")
    terminal.insert('end', "-------------------------------\n")

    try:
        if not target.startswith(("http://", "https://")):
            target = "http://" + target

        with open(wordlist, 'r') as wl:
            words = [word.strip() for word in wl if word.strip()]  # Get all non-empty words from the wordlist
            progress["maximum"] = len(words)  # Set the maximum value of the progress bar to the total number of words
            progress["value"] = 0  # Initialize progress bar value to 0
            
            for word in words:
                if use_agent_rotation:
                    headers['User-Agent'] = random.choice(USER_AGENTS)
                
                url_dir = f"{target}/{word}/"
                try:
                    response = requests.get(url_dir, headers=headers)
                    terminal.insert('end', f"Trying {url_dir}...\n", 'white')
                    auto_scroll(terminal)
                    if response.status_code in [200, 403, 301, 302]:
                        terminal.insert('end', "[+] ", 'green_bold')
                        terminal.insert('end', f"Found directory: {url_dir}\n")
                        found_items.append(url_dir)
                        if use_recursive_scanning:
                            dirbust(url_dir, wordlist, terminal, use_agent_rotation, use_random_delay, use_recursive_scanning, use_extensions_var, progress, tooltip)
                except requests.RequestException as e:
                    terminal.insert('end', f"Error accessing {url_dir}: {str(e)}\n")

                for ext in extensions:
                    url_ext = f"{target}/{word}.{ext}"
                    try:
                        response = requests.get(url_ext, headers=headers)
                        terminal.insert('end', f"Trying {url_ext}...\n", 'white')
                        if response.status_code == 200:
                            terminal.insert('end', f"Found: {url_ext}\n")
                            found_items.append(url_ext)
                    except requests.RequestException as e:
                        terminal.insert('end', f"Error accessing {url_ext}: {str(e)}\n")

                if use_random_delay:
                    time.sleep(random.uniform(1, 5))

                # Increment the progress bar value by one after processing each word
                progress["value"] += 1
                show_progress_percentage(None, progress, tooltip)  # Updated to refresh the tooltip
                progress.update()

                if stop_dirbusting:
                    terminal.insert('end', "\n-------\n")
                    terminal.insert('end', "STOPPED\n")
                    terminal.insert('end', "-------\n")
                    if found_items:
                        terminal.insert('end', "\nItems Found:\n", 'yellow_bold')
                        for item in found_items:
                            terminal.insert('end', f"{item}\n", 'yellow_bold')
                    else:
                        terminal.insert('end', "No items were found.\n", 'yellow_bold')
                    break
    except Exception as e:
        terminal.insert('end', f"An error occurred: {str(e)}\n")

    play_sound(os.path.join('media', 'sounds', 'pass_cracked_sfx.wav'))


def stop_dirbusting_process(terminal):
    global stop_dirbusting
    stop_dirbusting = True
    terminal.insert('end', "\n! ! ! ! ! ! ! ! ! ! ! ! ! !\n")
    terminal.insert('end', "Terminating..\n")
    terminal.insert('end', "! ! ! ! ! ! ! ! ! ! ! ! ! !\n\n")

def export_results():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        with open(filename, "w") as f:
            for item in found_items:
                f.write(item + "\n")

def show_tooltips(widget, text):
    
    tooltip = None
    after_id = None
    disappear_after_id = None

    def position_tooltip():
        nonlocal tooltip, disappear_after_id
        if tooltip:
            tooltip.destroy()
            if disappear_after_id:
                widget.after_cancel(disappear_after_id)
    
        tooltip = Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        label = Label(tooltip, text=text, bg='yellow', padx=5, pady=0)
        label.pack()
        x, y, _, _ = widget.bbox("insert")
        y += widget.winfo_height()
        x += widget.winfo_rootx() + 15   # added + 15 for some offset
        y += widget.winfo_rooty() + 20   # added + 20 for some offset
        tooltip.geometry(f"+{x}+{y}")
        tooltip.bind("<Leave>", leave)   # Bind the leave event to the tooltip itself as well
    
        # Set a timer for the tooltip to disappear after 2 seconds
        disappear_after_id = widget.after(2000, lambda: tooltip.destroy() if tooltip else None)
        
    def enter(event):
        nonlocal after_id
        # Delay the tooltip display by 150ms
        after_id = widget.after(150, position_tooltip)
    
    def leave(event):
        nonlocal tooltip, after_id
        if after_id:
            # If there's a scheduled tooltip display, cancel it.
            widget.after_cancel(after_id)
            after_id = None
        
        if tooltip:
            # Check if the mouse is not within the tooltip's or widget's bounding box
            if not (tooltip.winfo_x() < event.x_root < tooltip.winfo_x() + tooltip.winfo_width() and 
                    tooltip.winfo_y() < event.y_root < tooltip.winfo_y() + tooltip.winfo_height()) and \
               not (widget.winfo_x() < event.x_root < widget.winfo_x() + widget.winfo_width() and 
                    widget.winfo_y() < event.y_root < widget.winfo_y() + widget.winfo_height()):
                tooltip.destroy()
                tooltip = None

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

    return tooltip


def show_progress_percentage(event, progress, tooltip=None):
    percentage = (progress["value"]/progress["maximum"]) * 100
    tooltip_text = f"{percentage:.2f}% completed"
    
    # If tooltip already exists, just update its label. Otherwise, create a new tooltip.
    if tooltip:
        tooltip.children['!label'].config(text=tooltip_text)
    else:
        show_tooltips(progress, tooltip_text)



def print_instructions(terminal):
    instructions = """




================================================= HUNTR DIRECTORY BUSTER INSTRUCTIONS ===============================================

[Purpose]
A tool to perform directory busting on web servers. Use ethically and with authorization.

[Procedure]

1. Target URL: Enter the web server's URL.
2. Wordlist: Choose a predefined list or select 'Use custom wordlist' for your own.
3. Options:
   - Rotate User-Agent: Switch User-Agent per request.
   - Random Delay: Add random pauses between requests.
   - Recursive Scanning: Dive into found directories.
   - Enable Extensions: Check for common file extensions.
4. Click "START" to begin and "STOP" to halt.
5. Monitor progress in the terminal and via the progress bar.
6. Results:
   - Use "EXPORT RESULTS" to save findings.
7. "X" button: Return to the previous frame.

Note: Always get proper permissions before using.

=====================================================================================================================================
"""
    terminal.insert('end', instructions, ('centered', 'white'))

def create_dirbuster_frame(root, open_frame, reconnaissance_frame, button_font):
    def on_enter(e):
        e.widget['background'] = 'white'
        e.widget['foreground'] = 'black'

    def on_leave(e):
        e.widget['background'] = 'red'
        e.widget['foreground'] = 'black'

    dirbuster_frame = Frame(root, bg='gray3')
    # CREATE ANIMATION INSTANCE HERE
    dynamic_text_canvas = DynamicTextCanvas(dirbuster_frame, bg='gray3', width=400, height=60)
    dynamic_text_canvas.pack(pady=0)
    
    terminal_frame = Frame(dirbuster_frame, bg='gray3')
    terminal_frame.pack(pady=0)
    

    target_label = Label(terminal_frame, text="ENTER TARGET:", bg='gray3', fg='red', font=('System', 10))
    target_label.grid(row=0, column=0)

    target_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    target_entry.grid(row=0, column=1)

    default_wordlist = os.path.join("Wordlists", "1000_top_subdomains.txt")
    wordlist_combobox = ttk.Combobox(terminal_frame, values=[default_wordlist, "Use custom wordlist"], state="readonly", width=25)
    wordlist_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=wordlist_combobox: on_wordlist_selection(event, combobox))
    wordlist_combobox.set(default_wordlist)
    wordlist_combobox.grid(row=0, column=2)

    agent_rotation_var = IntVar()
    random_delay_var = IntVar()
    recursive_scan_var = IntVar()
    use_extensions_var = IntVar()

    agent_rotation_check = Checkbutton(terminal_frame, text="Rotate User-Agent", variable=agent_rotation_var, bg='gray3', fg='red')
    agent_rotation_check.grid(row=3, column=0)
    show_tooltips(agent_rotation_check, "Toggle rotating User-Agent for each request.")

    random_delay_check = Checkbutton(terminal_frame, text="Random Delay", variable=random_delay_var, bg='gray3', fg='red')
    random_delay_check.grid(row=3, column=1)
    show_tooltips(random_delay_check, "Adds a random delay between requests.")

    recursive_scan_check = Checkbutton(terminal_frame, text="Recursive Scanning", variable=recursive_scan_var, bg='gray3', fg='red')
    recursive_scan_check.grid(row=3, column=2)
    show_tooltips(recursive_scan_check, "If a directory is found, it will scan inside that directory recursively.")

    extensions_check = Checkbutton(terminal_frame, text="Enable Extensions", variable=use_extensions_var, bg='gray3', fg='red')
    extensions_check.grid(row=3, column=3)

    style = Style()
    style.theme_use('default')
    style.configure("TProgressbar", thickness=25, troughcolor='gray3', background='red', relief='flat')
    progress = Progressbar(terminal_frame, style="TProgressbar", orient="horizontal", length=300, mode="determinate")
    tooltip = None  # Define tooltip variable outside of functions
    progress.bind("<Enter>", lambda event, progress=progress: show_progress_percentage(event, progress))
    progress.grid(row=4, column=0, columnspan=2, pady=0)

    start_button = Button(terminal_frame, text="START", fg="black", bg="red", relief=FLAT, font=('System', 10), 
                          command=lambda: threading.Thread(target=dirbust, args=(
                              target_entry.get(), wordlist_combobox.get(), terminal,
                              agent_rotation_var.get(), random_delay_var.get(), recursive_scan_var.get(), use_extensions_var, progress
                          )).start())
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)
    start_button.grid(row=0, column=3)

    stop_button = Button(terminal_frame, text="STOP", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: stop_dirbusting_process(terminal))
    stop_button.bind("<Enter>", on_enter)
    stop_button.bind("<Leave>", on_leave)
    stop_button.grid(row=0, column=4)

    # The new Clear Terminal button
    clear_button = Button(terminal_frame, text="CLEAR TERMINAL", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)
    clear_button.grid(row=4, column=4)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 12, 'bold'), command=lambda: open_frame(dirbuster_frame, reconnaissance_frame, "reconnaissance"))
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=0, column=5)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.tag_configure('yellow_bold', foreground='yellow', font=('System', 10, 'bold'))
    terminal.tag_configure('green_bold', foreground='green', font=('System', 10, 'bold'))
    terminal.tag_configure('white', foreground='white', font=('Consolas', 9))  # Defining the white tag here
    terminal.grid(row=2, column=0, columnspan=6, pady=10)


    # Define the centered tag here
    terminal.tag_configure('centered', justify='center')

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))

    export_button = Button(terminal_frame, text="EXPORT RESULTS", fg="black", bg="red", relief=FLAT, font=('System', 10), command=export_results)
    export_button.bind("<Enter>", on_enter)
    export_button.bind("<Leave>", on_leave)
    export_button.grid(row=4, column=5)

    print_instructions(terminal)

    return dirbuster_frame
