from tkinter import *
from tkinter import ttk
import threading
import keyboard
from datetime import datetime, timedelta
import time
import winsound

trigger_key = "A"
countdown_timer = "00:00:00"
alarm_time = "10"

def disable_input():
    trigger_key_input.config(state = 'disabled')
    countdown_timer_input.config(state = 'disabled')
    alarm_time_input.config(state = 'disabled')

def save(key, countdown, alarm):
    global trigger_key, countdown_timer, alarm_time
    trigger_key = key
    countdown_timer = countdown
    alarm_time = alarm
    disable_input()
    trigger()

def trigger():
    split_time = countdown_timer.split(":")
    cnt_dwn_hours = int(split_time[0])
    cnt_dwn_minutes = int(split_time[1])
    cnt_dwn_seconds = int(split_time[2])
    while True:
        if keyboard.is_pressed(trigger_key):
            print ("Triggered")
            now = datetime.now()
            alarm_at = now + timedelta(hours=cnt_dwn_hours, minutes=cnt_dwn_minutes, seconds=cnt_dwn_seconds)
            delay = (alarm_at - now).total_seconds()
            threading.Timer(delay, alarm).start()
            break

def alarm():
    print('Alarm!')
    winsound.PlaySound('alarm.wav', winsound.SND_ASYNC)
    loop_timer = time.time() + int(alarm_time)
    while True:
        if time.time() > loop_timer:
            winsound.PlaySound(None, winsound.SND_PURGE)
            break
    trigger()
    print ("Done")

root = Tk()
root.title('Key Alarm')
root.geometry('400x150')
icon = PhotoImage(file = 'alarm.png')
root.iconphoto(False, icon)

trigger_key_label = Label(root, text = "Trigger key", width = 22, anchor = 'w')
trigger_key_input = Entry(root, width = 20)
trigger_key_input.insert(0, "A")

countdown_timer_label = Label(root, text = "Countdown time (hh:mm:ss)", width = 22, anchor = 'w')
countdown_timer_input = Entry(root, width = 20)
countdown_timer_input.insert(0, "00:00:00")

alarm_time_label = Label(root, text = "Alarm timeout (ss)", width = 22, anchor = 'w')
alarm_time_input = Entry(root, width = 20)
alarm_time_input.insert(0, "10")

start_button = Button(root, text = "Save", command = lambda: save(trigger_key_input.get(), countdown_timer_input.get(), alarm_time_input.get()))

trigger_key_label.grid(row = 0, column = 0, padx = 10, pady = 2.5)
trigger_key_input.grid(row = 0, column = 1, padx = 10, pady = 2.5)
countdown_timer_label.grid(row = 1, column = 0, padx = 10, pady = 2.5)
countdown_timer_input.grid(row = 1, column = 1, padx = 10, pady = 2.5)
alarm_time_label.grid(row = 2, column = 0, padx = 10, pady = 2.5)
alarm_time_input.grid(row = 2, column = 1, padx = 10, pady = 2.5)
start_button.grid(row = 3, column = 1, padx = 10, pady = 2.5)

root.mainloop()