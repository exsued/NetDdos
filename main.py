from tkinter import *
from tkinter import ttk
from RangeSlider.RangeSlider import RangeSliderH
import subprocess
import os
import sys

def add_button_click():
    INPUT = new_address_input.get("1.0", "end-1c")
    if(not(INPUT.isspace() or (len(INPUT) == 0))):
        targets_listBox.insert(END, INPUT)
    new_address_input.delete(1.0,END)

def remove_button_click():
    if(len(targets_listBox.curselection()) > 0):
        targets_listBox.delete(targets_listBox.curselection()[0])

def start_button_click():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    os.path.join(application_path, "ddos")
    result = subprocess.run([sys.executable], capture_output=True, text=True)

win = Tk()

photo = PhotoImage(file="logo.png")
win.iconphoto(False, photo)
win.config(bg="white")
#win.geometry(f"700x400")
win.resizable(False, False)


canvas = Canvas(win, width=510, height=350)
canvas.pack()

####################  LEFT SIZE  ##################
label_targets_ip = Label(canvas, text="Targets IP:")
label_targets_ip.place(x=35, y=0)

targets_listBox = Listbox(canvas, width=21)
targets_listBox.place(x=0, y=20)

#_______________________
new_address_input = Text(canvas, height = 1, width = 21)
new_address_input.place(x=0, y=205)

add_target_button = Button(canvas, text="+", command=add_button_click)
add_target_button.place(x=0, y=230, width=70)

remove_target_button = Button(canvas, text="-", command=remove_button_click)
remove_target_button.place(x=80, y=230, width=70)

start_button = Button(canvas, text="Start", command=start_button_click)
start_button.place(x=0, y=280, width=150)

targets_listBox.insert(END, "192.168.0.1")
targets_listBox.insert(END, "127.0.0.1")
###################################################

###################  RIGHT SIZE  ##################

label_packet_size = Label(canvas, text="Packet size(bytes):")
label_packet_size.place(x=205, y=0)

useTCP = BooleanVar()
useTCP.set(0)
useUDP = BooleanVar()
useUDP.set(0)
useICMP = BooleanVar()
useICMP.set(0)

tcp_check = Checkbutton(canvas, text="TCP", variable=useTCP, onvalue=1, offvalue=0)
tcp_check.place(x=190, y=35)
tcp_check = Checkbutton(canvas, text="UDP", variable=useUDP, onvalue=1, offvalue=0)
tcp_check.place(x=190, y=100)
tcp_check = Checkbutton(canvas, text="ICMP", variable=useICMP, onvalue=1, offvalue=0)
tcp_check.place(x=190, y=165)

min_tcp_size = IntVar()  #left handle variable
max_tcp_size = IntVar()  #right handle variable

tcp_size_slider = RangeSliderH(canvas, [min_tcp_size, max_tcp_size], Height=50, Width=240, min_val=64, max_val=1024, padX=11, font_size=8, digit_precision='.0f' )
tcp_size_slider.place(x=260, y=25)

min_udp_size = IntVar()  #left handle variable
max_udp_size = IntVar()  #right handle variable

udp_size_slider = RangeSliderH(canvas, [min_udp_size, max_udp_size], Height=50, Width=240, min_val=64, max_val=1024, padX=11, font_size=8, digit_precision='.0f' )
udp_size_slider.place(x=260, y=90)

min_icmp_size = IntVar()  #left handle variable
max_icmp_size = IntVar()  #right handle variable

icmp_size_slider = RangeSliderH(canvas, [min_icmp_size, max_icmp_size], Height=50, Width=240, min_val=64, max_val=1024, padX=11, font_size=8, digit_precision='.0f' )
icmp_size_slider.place(x=260, y=155)

label_packet_size = Label(canvas, text="Interval(seconds):")
label_packet_size.place(x=205, y=240)

min_interval = DoubleVar()  #left handle variable
max_interval = DoubleVar()  #right handle variable

interval_slider = RangeSliderH(canvas, [min_interval, max_interval], Height=50, Width=150, min_val=0.1, max_val=5, padX=11, font_size=8, digit_precision='.1f' )
interval_slider.place(x=260, y=260)

###################################################
win.mainloop()
