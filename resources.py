from tkinter import Frame, Button, Label, BOTTOM, FLAT
from webbrowser import open_new
import tkinter.font as font

def on_enter(e):
    e.widget['background'] = 'white'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'black'

def create_resources_frame(root, open_frame, main_frame, button_font):
    resources_frame = Frame(root, bg='gray3')

    def bind_hover_effect(button):
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=15)

    pentest_monkey_button = Button(resources_frame, text="PENTEST MONKEY", command=lambda: open_new('https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(pentest_monkey_button)
    pentest_monkey_button.pack(pady=0)

    Label(resources_frame, text="Provides commands for generating reverse shells, useful for establishing backdoors.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    exploit_db_button = Button(resources_frame, text="EXPLOIT-DB", command=lambda: open_new('https://www.exploit-db.com/'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(exploit_db_button)
    exploit_db_button.pack(pady=0)

    Label(resources_frame, text="A database of known exploits and vulnerabilities applicable to specific systems.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    shodan_search_button = Button(resources_frame, text="SHODAN SEARCH", command=lambda: open_new('https://www.shodan.io/'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(shodan_search_button)
    shodan_search_button.pack(pady=0)

    Label(resources_frame, text="A search engine for internet-connected devices, useful for identifying potential targets.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    censys_search_button = Button(resources_frame, text="CENSYS SEARCH", command=lambda: open_new('https://search.censys.io/'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(censys_search_button)
    censys_search_button.pack(pady=0)

    Label(resources_frame, text="Similar to Shodan but with more depth, helps in discovering and monitoring internet-connected devices.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    gtfobins_button = Button(resources_frame, text="GTFOBINS", command=lambda: open_new('https://gtfobins.github.io/'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(gtfobins_button)
    gtfobins_button.pack(pady=0)

    Label(resources_frame, text="A list of Unix binaries that can be exploited for bypassing local security restrictions, handy for privilege escalation.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    cyberchef_button = Button(resources_frame, text="CYBERCHEF", command=lambda: open_new('https://gchq.github.io/CyberChef/'), fg="black", bg="red", font=button_font, relief=FLAT)
    bind_hover_effect(cyberchef_button)
    cyberchef_button.pack(pady=0)

    Label(resources_frame, text="A multipurpose tool for data analysis, encoding, encryption, useful for handling encoded data or creating payloads.", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="_________________________________________", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)
    Label(resources_frame, text="", bg='gray3', fg='red', font=('System', 10)).pack(pady=0)

    back_button_font = font.Font(family="System", size=12)
    back_button = Button(resources_frame, text="X", command=lambda: open_frame(resources_frame, main_frame, "huntr"), fg="black", bg="red", font=back_button_font, relief=FLAT, height=1, width=2)
    bind_hover_effect(back_button)
    back_button.pack(side=BOTTOM, anchor="center", padx=5, pady=5)

    return resources_frame
