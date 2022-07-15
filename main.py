from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from RangeSlider.RangeSlider import RangeSliderH
import threading
import subprocess
import os
import sys
from datetime import datetime
import socket

class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode)
    def __del__(self):
        self.file.close()
    def mywrite(self, data):
        print(data)
        self.file.write(str(data)+"\n")
    def flush(self):
        self.file.flush()

tee = Tee("session " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ".txt", "w")

def add_button_click():
    INPUT = new_address_input.get("1.0", "end-1c")
    if(not(INPUT.isspace() or (len(INPUT) == 0))):
        targets_listBox.insert(END, INPUT)
    new_address_input.delete(1.0,END)

def remove_button_click():
    if(len(targets_listBox.curselection()) > 0):
        targets_listBox.delete(targets_listBox.curselection()[0])

cmd = None

def execBackEnd(dests, tcpEnabled, udpEnabled):
    global cmd
    global tee
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    application_path = os.path.join(application_path, "ddos")
    args = ["-source"]
    args.append("127.0.0.1")
    args.append("-destination")
    args.append(','.join(dests))
    if(tcpEnabled == 1):
        args.append("-tcp")
    if(udpEnabled == 1):
        args.append("-udp")
    args.insert(0, application_path)
    tee.mywrite("run: " + str(args))
    #args = ["-source", "192.168.0.1", "-destination", "192.168.10.8", "-intervalTCP", "1", "-tcp", "-udp"]
    cmd = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        tee.mywrite(line.decode('utf-8').rstrip("\n"))
    cmd.wait()  # you may already be handling this in your current code

def on_closing():
    global tee
    if t != None:
        t.do_run = False
        cmd.kill()
        backEndRunning = False
    if messagebox.askokcancel("Quit", "Do you want to quit (log saves after quit)?"):
        win.destroy()
    print("Log file saved")

backEndRunning = False
t = None

def start_button_click():
    global backEndRunning
    global t
    if backEndRunning:
        t.do_run = False
        cmd.kill()
        start_button.config(text="Start")
        backEndRunning = False
    else:
        destinations = targets_listBox.get(0, END)
        t = threading.Thread(target=execBackEnd, args=[destinations, useTCP.get(), useUDP.get()])
        t.start()
        start_button.config(text="Stop")
        backEndRunning = True

win = Tk()

photo = PhotoImage(file="logo.png")
win.iconphoto(False, photo)
win.config(bg="white")
#win.geometry(f"700x400")
win.resizable(False, False)

win.protocol("WM_DELETE_WINDOW", on_closing)

canvas = Canvas(win, width=800, height=350)
canvas.pack()

####################  LEFT SIZE  ##################
label_source_ip = Label(canvas, text="Source IP:")
label_source_ip.place(x=35, y=0)

source_listBox = Listbox(canvas, width=21)
source_listBox.place(x=0, y=20)

label_targets_ip = Label(canvas, text="Targets IP:")
label_targets_ip.place(x=200, y=0)

targets_listBox = Listbox(canvas, width=21)
targets_listBox.place(x=165, y=20)

#_______________________
new_src_address_input = Text(canvas, height = 1, width = 21)
new_src_address_input.place(x=0, y=205)

add_source_button = Button(canvas, text="+", command=add_button_click)
add_source_button.place(x=0, y=230, width=70)

remove_source_button = Button(canvas, text="-", command=remove_button_click)
remove_source_button.place(x=80, y=230, width=70)

#_____________

new_address_input = Text(canvas, height = 1, width = 21)
new_address_input.place(x=164, y=205)

add_target_button = Button(canvas, text="+", command=add_button_click)
add_target_button.place(x=164, y=230, width=70)

remove_target_button = Button(canvas, text="-", command=remove_button_click)
remove_target_button.place(x=244, y=230, width=70)

start_button = Button(canvas, text="Start", command=start_button_click)
start_button.place(x=0, y=280, width=150)

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

source_listBox.insert(END, IPAddr)
#targets_listBox.insert(END, "192.168.0.1")
###################################################

###################  RIGHT SIZE  ##################

label_packet_size = Label(canvas, text="Packet size(bytes):")
label_packet_size.place(x=405, y=0)

useTCP = IntVar()
useUDP = IntVar()
useICMP = IntVar()

tcp_check = Checkbutton(canvas, text="TCP", variable=useTCP, onvalue=1, offvalue=0)
tcp_check.place(x=390, y=35)
tcp_check = Checkbutton(canvas, text="UDP", variable=useUDP, onvalue=1, offvalue=0)
tcp_check.place(x=390, y=100)
tcp_check = Checkbutton(canvas, text="ICMP", variable=useICMP, onvalue=1, offvalue=0)
tcp_check.place(x=390, y=165)

min_tcp_size = DoubleVar()  #left handle variable
max_tcp_size = DoubleVar()  #right handle variable

tcp_size_slider = RangeSliderH(canvas, [min_tcp_size, max_tcp_size], Height=50, Width=300, min_val=64, max_val=1500, padX=11, font_size=8, digit_precision='.0f' )
tcp_size_slider.place(x=460, y=25)

min_udp_size = DoubleVar()  #left handle variable
max_udp_size = DoubleVar()  #right handle variable

udp_size_slider = RangeSliderH(canvas, [min_udp_size, max_udp_size], Height=50, Width=300, min_val=64, max_val=1500, padX=11, font_size=8, digit_precision='.0f' )
udp_size_slider.place(x=460, y=90)

min_icmp_size = DoubleVar()  #left handle variable
max_icmp_size = DoubleVar()  #right handle variable

icmp_size_slider = RangeSliderH(canvas, [min_icmp_size, max_icmp_size], Height=50, Width=300, min_val=64, max_val=1500, padX=11, font_size=8, digit_precision='.0f' )
icmp_size_slider.place(x=460, y=155)

label_packet_size = Label(canvas, text="Interval(seconds):")
label_packet_size.place(x=405, y=240)

min_interval = DoubleVar()  #left handle variable
max_interval = DoubleVar()  #right handle variable

interval_slider = RangeSliderH(canvas, [min_interval, max_interval], Height=50, Width=150, min_val=0.1, max_val=5, padX=11, font_size=8, digit_precision='.1f' )
interval_slider.place(x=460, y=260)

###################################################
win.mainloop()
