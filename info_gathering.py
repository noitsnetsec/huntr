#info_gathering.py (info gathering file)
from tkinter import Frame, Text, Button, Entry, Label, StringVar, OptionMenu, messagebox, FLAT
import requests
from bs4 import BeautifulSoup
import threading
import os
import socket
from ipwhois import IPWhois
import ipaddress
import random
import tkinter as tk

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

class DynamicTextCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.font = ('Consolas', 11, 'bold')
        self.text_positions = []
        self.text_values = list("WHOIS+")  # Setting the text to "PING SCAN"
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

def get_whois_data(domain):
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("whois.iana.org", 43))
        s.send((domain + "\r\n").encode())

        response = b""
        while True:
            data = s.recv(4096)
            response += data
            if not data:
                break
        s.close()
        return response.decode()

    except Exception as e:
        return str(e)

def get_geolocation(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    return response.json()

def get_headers(url):
    if not url.startswith('http'):
        url = 'http://' + url
    response = requests.get(url)
    return response.headers

def get_subnet(ip):
    return ipaddress.ip_network(ip, strict=False)

def get_ip_by_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        return None

def get_domain_by_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror as e:
        return None

def toggle_dns_ip(target_entry, dns_to_ip_button, original_target):
    current_value = target_entry.get()

    # Check if the current_value is an IP or DNS
    try:
        ipaddress.ip_address(current_value)  # Throws an exception if not an IP
        is_ip = True
    except ValueError:
        is_ip = False

    if is_ip:
        # If it's an IP, we try to reverse it to DNS, but first check if we have an original DNS
        if original_target[0]:
            new_target_value = original_target[0]
            dns_to_ip_button['text'] = "DNS to IP"
        else:
            messagebox.showerror("Error", "Cannot find original DNS for the IP.")
            return
    else:
        # It's a DNS, so we convert to IP
        new_target_value = get_ip_by_domain(current_value)
        if not new_target_value:
            messagebox.showerror("Invalid DNS", "The DNS could not be resolved.")
            return
        original_target[0] = current_value
        dns_to_ip_button['text'] = "IP to DNS"

    target_entry.delete(0, 'end')
    target_entry.insert(0, new_target_value)


def info_gathering(target, gather_type, terminal):
    def run():
        terminal.delete('1.0', 'end')
        terminal.insert('end', '-'*40 + '\n')
        terminal.insert('end', f'### {gather_type} Selected ###\n')
        terminal.insert('end', '-'*40 + '\n')

        if gather_type == 'WHOIS Domain Lookup':
            result = get_whois_data(target)

        elif gather_type == 'WHOIS IP Lookup':
            obj = IPWhois(target)
            result = obj.lookup_whois()

        elif gather_type == 'Reverse DNS':
            result = socket.gethostbyaddr(target)

        elif gather_type == 'IP Geolocation':
            result = get_geolocation(target)

        elif gather_type == 'HTTP Headers':
            result = get_headers(target)

        elif gather_type == 'Subnet Calculator':
            result = get_subnet(target)

        terminal.insert('end', str(result))
    
    threading.Thread(target=run, daemon=True).start()

def clear_terminal(terminal):
    terminal.delete('1.0', 'end')

def create_info_gathering_frame(root, open_frame, reconnaissance_frame, button_font):
    gather_types = {
        '<Select Method>': {
            'description': ''
        },
        'WHOIS Domain Lookup': {
            'description': 'Performs a WHOIS lookup for a domain using a custom Python function.'
        },
        'WHOIS IP Lookup': {
            'description': 'Performs a WHOIS lookup for an IP address using ipwhois library.  (use ipv4)'
        },
        'Reverse DNS': {
            'description': 'Performs a reverse DNS lookup using socket library.'
        },
        'IP Geolocation': {
            'description': 'Performs an IP geolocation lookup using ip-api.com.'
        },
        'HTTP Headers': {
            'description': 'Inspects the HTTP headers of a URL using requests library.'
        },
        'Subnet Calculator': {
            'description': 'Calculates the subnet of an IP address using ipaddress library. (use ipv4)'
        }
    }

    def update_description(*args):
        description_label.config(text=gather_types[gather_type.get()]['description'])

    original_target = [None]

    info_gathering_frame = Frame(root, bg='gray3')
        # Create an instance of the DynamicTextCanvas and pack it
    dynamic_text = DynamicTextCanvas(info_gathering_frame, bg='gray3', width=800, height=60)
    dynamic_text.pack(pady=0)

    terminal_frame = Frame(info_gathering_frame, bg='gray3')
    terminal_frame.pack(pady=0)
    terminal_frame = Frame(info_gathering_frame, bg='gray3')
    terminal_frame.pack(pady=0)

    target_label = Label(terminal_frame, text="ENTER TARGET:", bg='gray3', fg='red', font=('System', 10))
    target_label.grid(row=0, column=0)

    target_entry = Entry(terminal_frame, width=30, bg='gray3', fg='red')
    target_entry.grid(row=0, column=1)

    # Declare gather_type here before using it
    gather_type = StringVar()
    gather_type.set('<Select Method>')
    gather_type.trace('w', update_description)

    dns_to_ip_button = Button(terminal_frame, text="← DNS > IPv4", command=lambda: toggle_dns_ip(target_entry, dns_to_ip_button, original_target), relief=FLAT, fg="black", bg="red", font=('System', 10))
    dns_to_ip_button.bind("<Enter>", on_enter)
    dns_to_ip_button.bind("<Leave>", on_leave)
    dns_to_ip_button.grid(row=0, column=2)

    gather_optionmenu = OptionMenu(terminal_frame, gather_type, *gather_types.keys())
    gather_optionmenu.config(font=('System', 10), fg='black', bg='red')
    gather_optionmenu.grid(row=0, column=3, padx=20)

    gather_button = Button(terminal_frame, text="SCAN", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: info_gathering(target_entry.get(), gather_type.get(), terminal))
    gather_button.bind("<Enter>", on_enter)
    gather_button.bind("<Leave>", on_leave)
    gather_button.grid(row=0, column=4)

    clear_button = Button(terminal_frame, text="CLEAR", fg="black", bg="red", relief=FLAT, font=('System', 10), command=lambda: clear_terminal(terminal))
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)
    clear_button.grid(row=0, column=5)

    back_button = Button(terminal_frame, text="X", fg="black", bg="red", relief=FLAT, font=('System', 10, 'bold'), command=lambda: open_frame(info_gathering_frame, reconnaissance_frame, "reconnaissance"), height=1, width=3)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    back_button.grid(row=0, column=6)

    description_label = Label(terminal_frame, text='', bg='gray3', fg='red', font=('System', 10))
    description_label.grid(row=1, column=0, columnspan=7)

    terminal = Text(terminal_frame, width=120, height=32, bg='gray3', fg='red', bd=2)
    terminal.grid(row=2, column=0, columnspan=7, pady=10)

    terminal.bind("<Key>", ignore_input)
    terminal.bind('<Control-c>', lambda event: copy_text(event, terminal, root))

    return info_gathering_frame
