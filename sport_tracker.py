import tkinter as tk
from tkinter import DISABLED, END, NORMAL, messagebox, ttk
import sqlite3 as db
import datetime
from matplotlib import pyplot as plt

# create new database
conn = db.connect('track_records.db')
cur = conn.cursor()
cur.execute(""" CREATE TABLE IF NOT EXISTS track_records
    (
        date VARCHAR NOT NULL,
        activity VARCHAR NOT NULL,
        distance INT NOT NULL
    ); """)
cur.close()
conn.commit()
conn.close()

# create tkinter window
window = tk.Tk()
window.title('sport_tracker')
window.geometry('800x420')
window.iconbitmap('icon.ico')
window.config(background='light yellow')

title = tk.Label(window, text='Sport tracker', font='Arial 16 bold', background='light yellow')
title.grid(row=0, column=0, columnspan=3, ipadx=20, ipady=10)

add_frame = tk.LabelFrame(window, text='add record', labelanchor='n', background='light yellow')
add_frame.grid(row=1, column=0, columnspan=3, padx=5, sticky='ew')

date = tk.Label(add_frame, text='date', font='Arial 11', background='light yellow')
date.grid(row=2, column=0, pady=2)
fill_date = tk.Entry(add_frame, width=20, font='Arial 11', background='light pink')
fill_date.grid(row=3, column=0)
note_date = tk.Label(add_frame, text='YYYY-MM-DD', font='Arial 8', background='light yellow')
note_date.grid(row=4, column=0)

style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground= "light pink", background= "light pink")

activity = tk.Label(add_frame, text='activity', font='Arial 11', background='light yellow')
activity.grid(row=2, column=1, pady=2)
fill_activity = ttk.Combobox(add_frame, width=20, font='Arial 11', values=['running', 'biking', 'swimming'])
fill_activity.grid(row=3, column=1, padx=10)

distance = tk.Label(add_frame, text='distance', font='Arial 11', background='light yellow')
distance.grid(row=2, column=2, pady=2)
fill_distance = tk.Entry(add_frame, width=20, font='Arial 11', background='light pink')
fill_distance.grid(row=3, column=2)
note_distance = tk.Label(add_frame, text='in kilometers', font='Arial 8', background='light yellow')
note_distance.grid(row=4, column=2)

def add():    # add data to database
    conn = db.connect('track_records.db')
    cur = conn.cursor()
    inserted_data = f'date: {fill_date.get()} / activity: {fill_activity.get()} / distance: {fill_distance.get()}'
    if messagebox.askyesno(title='Warning', message=f'Data you have inserted: {inserted_data}, do you really want to save the record?') == True:
        cur.execute('INSERT INTO track_records (date, activity, distance) VALUES(?,?,?)', (fill_date.get(), fill_activity.get(), fill_distance.get()))
        messagebox.showinfo(title='Note', message='Record succesfuly added into database!')
        fill_date.delete(0, 'end')
        fill_activity.delete(0, 'end')
        fill_distance.delete(0, 'end')
    cur.close()
    conn.commit()
    conn.close()

add_btn = tk.Button(add_frame, width=10, text='add record', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=add)
add_btn.grid(row=3, column=3, padx=15)

######################

show_frame = tk.LabelFrame(window, text='show record', labelanchor='n', background='light yellow')
show_frame.grid(row=5, column=0, columnspan=2, padx=5, sticky='ew')

show_record = tk.Label(show_frame, text='show record from the day', font='Arial 11', background='light yellow')
show_record.grid(row=6, column=0, padx=10)
fill_day = tk.Entry(show_frame, width=20, font='Arial 11', background='light pink')
fill_day.grid(row=6, column=1)
note_day = tk.Label(show_frame, text='enter date (YYYY-MM-DD)', font='Arial 8', background='light yellow')
note_day.grid(row=7, column=1)

def show():    # show data from database (by certain date)
    conn = db.connect('track_records.db')
    cur = conn.cursor()
    day_selected = str(fill_day.get())
    cur.execute('SELECT activity, distance FROM track_records WHERE date = ?', ([day_selected]))
    record = cur.fetchall()
    if record == []:
        messagebox.showinfo(title='Note', message='You either entered wrong day format or that day you did not do anything!')  
    else:
        for index,record in enumerate(record):
            activity_label = tk.Label(show_frame, width=25, text=f'{record[0]} >>> {record[1]} km', anchor='w', font='Arial 11 bold', background='light yellow')
            activity_label.grid(row=8+index, column=0, columnspan=2)
    conn.commit()
    conn.close()

show_btn = tk.Button(show_frame, width=12, text='show record', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=show)
show_btn.grid(row=6, column=3, padx=10)

######################

def click(event):    # allow days entry
    fill_days.config(state='normal')
    fill_days.delete(0, 'end')

track_frame = tk.LabelFrame(window, text='show distance', labelanchor='n', background='light yellow')
track_frame.grid(row=13, column=0, columnspan=2, padx=5, sticky='ew')

show_track = tk.Label(track_frame, text='for the last', font='Arial 11', background='light yellow')
show_track.grid(row=14, column=0, padx=10)
fill_days = tk.Entry(track_frame, width=12, font='Arial 8', background='light pink')
fill_days.insert(0, 'enter number')
fill_days.config(state='disabled')
fill_days.bind('<Button-1>', click)
fill_days.grid(row=14, column=1)

show_track = tk.Label(track_frame, text='days you have covered this distance by ', font='Arial 11', background='light yellow')
show_track.grid(row=14, column=2, padx=10)
fill_activity_graph = ttk.Combobox(track_frame, width=12, font='Arial 11', values=['running', 'biking', 'swimming'])
fill_activity_graph.insert(0, 'choose one')
fill_activity_graph.grid(row=14, column=3, padx=10)

show_distance = tk.Label(track_frame, text='', font='Arial 32', background='light yellow')
show_distance.grid(row=14, column=4, rowspan=3, padx=20)


def grab_data():    # return data (distance and date) depending on user input - can choose activity from combobox and fill days interval
    today = datetime.date.today()
    time_track = int(fill_days.get())
    start_day = today - datetime.timedelta(days=time_track)

    conn = db.connect('track_records.db')
    cur = conn.cursor()
    cur.execute('SELECT date, distance FROM track_records WHERE date > ? and activity = ? ORDER BY date', ([start_day, fill_activity_graph.get()]))
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return data

def count():    # need to check entry (tests!)
    data = grab_data()
    total_dist = 0
    for date, distance in data:
        total_dist += distance
    show_distance.config(text=f'{total_dist}km!')

def graph():    # show graph with all records of chosen sport
    data = grab_data()
    dates = []
    distance = []
    for date, dist in data:
        dates.append(date)
        distance.append(dist)
    ### bar graph (needs to be polished - now really ugly, but working)
    fig = plt.figure(figsize=(10,5))
    plt.bar(dates, distance, color='turquoise', width=0.2)
    plt.xlabel('date')
    plt.ylabel('distance')
    plt.title('sport tracker')
    plt.show()


show_dist_btn = tk.Button(track_frame, width=12, text='show distance', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=count)
show_dist_btn.grid(row=15, column=2, padx=10, pady=5)

graph_btn = tk.Button(track_frame, width=12, text='show graph', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=graph)
graph_btn.grid(row=15, column=3, padx=10, pady=5)


window.mainloop()