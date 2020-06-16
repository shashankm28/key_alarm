from tkinter import *
from tkinter import ttk
import threading
import keyboard
from datetime import datetime, timedelta
import time
import winsound
import json
import sys

trigger_key = ""
countdown_timer = ""
alarm_time = ""
trigger_thread = None

def write_config_file(key, countdown, alarm):
    try:
        config = {
            "trigger_key" : key,
            "countdown_timer" : countdown,
            "alarm_time" : alarm
        }
        with open("config.json", "w") as output_file:
            json.dump(config, output_file)
        print ('Created config.json')
    except Exception as ex:
        print ("Error!")
        print (ex)

def initial_config_load():
    try:
        with open('config.json', 'r') as input_file:
            config = json.load(input_file)
        
        global trigger_key, countdown_timer, alarm_time
        trigger_key = config['trigger_key']
        countdown_timer = config['countdown_timer']
        alarm_time = config['alarm_time']
    except IOError as io_error:
        if io_error.errno == 2:
            write_config_file("F3","00:01:00","10")
        initial_config_load()
    except Exception as ex:
        print ("Error!")
        print (ex)

def disable_input():
    trigger_key_input.config(state = 'disabled')
    countdown_timer_input.config(state = 'disabled')
    alarm_time_input.config(state = 'disabled')

def enable_input():
    trigger_key_input.config(state = 'normal')
    countdown_timer_input.config(state = 'normal')
    alarm_time_input.config(state = 'normal')

def save(key, countdown, alarm):
    global trigger_key, countdown_timer, alarm_time
    trigger_key = key
    countdown_timer = countdown
    alarm_time = alarm
    write_config_file(key, countdown, alarm)

def trigger():
    global trigger_thread
    disable_input()

    trigger_key = trigger_key_input.get()
    countdown_timer = countdown_timer_input.get()
    
    split_time = countdown_timer.split(":")
    cnt_dwn_hours = int(split_time[0])
    cnt_dwn_minutes = int(split_time[1])
    cnt_dwn_seconds = int(split_time[2])
    while True:
        if keyboard.is_pressed(trigger_key):
            status_label.configure(text = "Triggered")
            now = datetime.now()
            alarm_at = now + timedelta(hours=cnt_dwn_hours, minutes=cnt_dwn_minutes, seconds=cnt_dwn_seconds)
            delay = (alarm_at - now).total_seconds()
            trigger_thread = threading.Timer(delay, alarm)
            trigger_thread.start()
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            break
        if keyboard.is_pressed('shift+x'):
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            if trigger_thread != None:
                trigger_thread = None
                status_label.configure(text = "Thread closed")
            enable_input()
            status_label.configure(text = "Press trigger button to start again!!")
            break

def alarm():
    status_label.configure(text = "Alarm!!")
    winsound.PlaySound('./assets/alarm.wav', winsound.SND_ASYNC)
    alarm_time = alarm_time_input.get()
    loop_timer = time.time() + int(alarm_time)
    while True:
        if time.time() > loop_timer:
            winsound.PlaySound(None, winsound.SND_PURGE)
            status_label.configure(text = "Press " + trigger_key + " to start again or shift+x to stop the background process.")
            break
    trigger()

initial_config_load()

root = Tk()
root.title('Key Alarm')
root.geometry('400x220')
icon = PhotoImage(file = './assets/alarm.png')
root.iconphoto(False, icon)

trigger_key_label = Label(root, text = "Trigger key", width = 22, anchor = 'w')
trigger_key_input = Entry(root, width = 20)
trigger_key_input.insert(0, trigger_key)

countdown_timer_label = Label(root, text = "Countdown time (hh:mm:ss)", width = 22, anchor = 'w')
countdown_timer_input = Entry(root, width = 20)
countdown_timer_input.insert(0, countdown_timer)

alarm_time_label = Label(root, text = "Alarm timeout (ss)", width = 22, anchor = 'w')
alarm_time_input = Entry(root, width = 20)
alarm_time_input.insert(0, alarm_time)

info_label_1 = Label(root, text = 'To stop background process/trigger press: shift+x')
info_label_2 = Label(root, text = 'To run again please press Trigger button again.')
info_label_3 = Label(root, text = 'Created by @shashankm28 (Github/Instagram)')

save_button = Button(root, text = "Save config", command = lambda: save(trigger_key_input.get(), countdown_timer_input.get(), alarm_time_input.get()))
trigger_button = Button(root, text = "Trigger", command = trigger)

trigger_key_label.grid(row = 0, column = 0, padx = 10, pady = 2.5)
trigger_key_input.grid(row = 0, column = 1, padx = 10, pady = 2.5)
countdown_timer_label.grid(row = 1, column = 0, padx = 10, pady = 2.5)
countdown_timer_input.grid(row = 1, column = 1, padx = 10, pady = 2.5)
alarm_time_label.grid(row = 2, column = 0, padx = 10, pady = 2.5)
alarm_time_input.grid(row = 2, column = 1, padx = 10, pady = 2.5)
save_button.grid(row = 3, column = 1, padx = 10, pady = 2.5, sticky = W)
trigger_button.grid(row = 3, column = 1, padx = 10, pady = 2.5, sticky = E)

info_label_1.grid(row = 4, column = 0, padx = 10, pady = 2.5, columnspan = 2 , sticky = W)
info_label_2.grid(row = 5, column = 0, padx = 10, pady = 2.5, columnspan = 2 , sticky = W)
info_label_3.grid(row = 6, column = 0, padx = 10, pady = 2.5, columnspan = 2 , sticky = W)

status_label = Label(root, width = 57, text = "STATUS", bd = 1, relief = SUNKEN, anchor = W)
status_label.grid(row = 7, column = 0, padx = 0, pady = 2.5, columnspan = 3 , sticky = W)

root.mainloop()