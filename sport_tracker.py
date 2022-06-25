import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3 as db
import matplotlib.pyplot as plt

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
    if tk.messagebox.askyesno(title='Warning', message=f'Data you have inserted: {inserted_data}, do you really want to save the record?') == True:
        cur.execute('INSERT INTO track_records (date, activity, distance) VALUES(?,?,?)', (fill_date.get(), fill_activity.get(), fill_distance.get()))
        tk.messagebox.showinfo(title='Note', message='Record succesfuly added into database!')
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
        tk.messagebox.showinfo(title='Note', message='You either entered wrong day format or that day you did not do anything!')  
    else:
        for index,record in enumerate(record):
            activity_label = tk.Label(show_frame, width=25, text=f'{record[0]} >>> {record[1]} km', anchor='w', font='Arial 11 bold', background='light yellow')
            activity_label.grid(row=8+index, column=0, columnspan=2)
    conn.commit()
    conn.close()

show_btn = tk.Button(show_frame, width=12, text='show record', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=show)
show_btn.grid(row=6, column=3, padx=10)

######################

show_graph_frame = tk.LabelFrame(window, text='show graph', labelanchor='n', background='light yellow')
show_graph_frame.grid(row=11, column=0, columnspan=2, padx=5, sticky='ew')

show_graph = tk.Label(show_graph_frame, text='choose the activity you would like \n to see a graph of records for', font='Arial 11', background='light yellow')
show_graph.grid(row=12, column=0, rowspan=2, padx=10)

fill_activity_graph = ttk.Combobox(show_graph_frame, width=20, font='Arial 11', values=['running', 'biking', 'swimming'])
fill_activity_graph.grid(row=12, column=1, padx=10, pady=2)

def graph():
    conn = db.connect('track_records.db')
    cur = conn.cursor()
    cur.execute('SELECT date, distance FROM track_records WHERE activity = ? ORDER BY date', ([fill_activity_graph.get()]))
    data = cur.fetchall()
    dates = []
    distance = []
    for value in data:
        dates.append(value[0])
        distance.append(value[1])
    cur.close()
    conn.commit()
    conn.close()
    ### bar graph (needs to be polished - now really ugly, but working)
    fig = plt.figure(figsize=(10,5))
    plt.bar(dates, distance, color='turquoise', width=0.2)
    plt.xlabel('date')
    plt.ylabel('distance')
    plt.title('sport tracker')
    plt.show()

graph_btn = tk.Button(show_graph_frame, width=12, text='show graph', font='Arial 11 bold', fg='dark blue', background='light grey', relief='raised', command=graph)
graph_btn.grid(row=12, column=2, padx=10, pady=5)

window.mainloop()

