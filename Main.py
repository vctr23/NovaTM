# %% 1. Head
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

# %% 2. Imports
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import datetime
import json
import Gestor_nova

# %% 3. Code
def count_tasks(task_treeview, label_task, label_completed_task):
    number_tasks = len(task_treeview.get_children())
    completed_task = sum(1 for task in task_treeview.get_children()
                         if task_treeview.item(task)["values"][2] == "Completed")

    label_task.configure(text=f"Total tasks: {number_tasks}")
    label_completed_task.configure(text=f"Completed tasks: {completed_task}")


def add_task(entry, list, task_treeview, label_task, label_completed_task):
    task = entry.get()
    priority = list.get()
    state = "Active"
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    edate = ""

    if len(task) != 0:
        task_treeview.insert("", "end", values=[task, priority, state, date, edate])
        count_tasks(task_treeview, label_task, label_completed_task)
        entry.delete(0, "end")
        return
    else:
        messagebox.showerror(
            title="ERROR", message="Error could not insert. Entry is empty.")
        return


def delete(task_treeview, label_task, label_completed_task):
    tasks = task_treeview.selection()
    if tasks:
        for task in tasks:
            task_treeview.delete(task)
        count_tasks(task_treeview, label_task, label_completed_task)
        messagebox.showinfo(
            title="Deleted", message="Row/s deleted correctly.")
    else:
        messagebox.showwarning(
            title="Warning", message="Select at least one row to delete.")


def import_from_json(task_treeview, label_task, label_completed_task):
    with open("examples.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
        if tasks:
            for task in tasks:
                task_treeview.insert("", "end", 
                                    values=[task["Task"], task["Priority"], 
                                        task["State"], task["Date"], task["EndDate"]])
        count_tasks(task_treeview, label_task, label_completed_task)


def mark_as_completed(task_treeview, label_task, label_completed_task):
    tasks = task_treeview.selection()
    edate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if tasks:
        for task in tasks:
            old_values = task_treeview.item(task, "values")
            task_treeview.item(task, values=(
                old_values[0], old_values[1], "Completed", old_values[3], edate))
        count_tasks(task_treeview, label_task, label_completed_task)

    else:
        messagebox.showwarning(
            title="Warning", message="Select at least one task to mark as completed.")


def edit_tasks(event, task_treeview, root):
    task = task_treeview.selection()
    if task:
            current_values = task_treeview.item(task)["values"]
            toplevel = Gestor_nova.Toplevel(root, current_values)
            toplevel.grab_set()
            root.wait_window(toplevel)

            if toplevel.result:
                task_name = toplevel.result.get("task_name", "").strip()
                priority = toplevel.result.get("priority", "Medium")  
                state = toplevel.result.get("state", "").strip()
                date = current_values[3]
                end_date = current_values[4]
                if task_name and state:
                    task_treeview.item(task, values = [task_name, priority, state, date, end_date])
                else:
                    messagebox.showwarning(
                        title="Warning", message = "Error. Task name or state are empty")
                    return
    else:
        messagebox.showwarning(
            title="Warning", message="Select at least one task to edit.")
        return


def change_appearance_mode(task_treeview, notebook, menu_treeview, tab2):
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        task_treeview["style"] = "Light.Treeview"
        notebook["style"] = "Light.TNotebook"
    else:
        ctk.set_appearance_mode("Dark")
        task_treeview["style"] = "Dark.Treeview"
        notebook["style"] = "Dark.TNotebook"
        
    menu_treeview.toggle_theme()   

    generate_gantt(tab2, task_treeview)


def generate_gantt(tab2, task_treeview):
    tasks = []
    start_dates = []
    end_dates = []

    for item in task_treeview.get_children():
        task, priority, state, sdate, edate = task_treeview.item(item)[
            "values"]
        start_date = pd.to_datetime(sdate)
        end_date = pd.to_datetime(edate)
        tasks.append(task)
        start_dates.append(pd.to_datetime(start_date))
        end_dates.append(pd.to_datetime(end_date))

    start_dates = pd.to_datetime(start_dates)
    end_dates = pd.to_datetime(end_dates)

    matplotlib.use("Agg") # Use of Agg to avoid conflicts with Tkinter

    if ctk.get_appearance_mode() == "Dark":
        plt.style.use('dark_background')
        bar_color = '#4A6984' 
        text_color = 'white'
    else:
        plt.style.use('default')
        bar_color = '#1F77B4'  
        text_color = 'black'

    cleanCanvas()
    fig, ax = plt.subplots(figsize=(3, 2))

    ax.barh(tasks, (end_dates - start_dates), left=start_dates, color = bar_color)

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45, fontsize = 8, color = text_color)
    plt.yticks(fontsize = 8, color = text_color)

    plt.title("Gantt chart", fontsize = 10, color = text_color)
    plt.xlabel("Date", fontsize = 8, color = text_color)
    plt.ylabel("Tasks", fontsize = 8, color = text_color)

    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.NSEW, ipady = 150)

    return canvas

def cleanCanvas():
    plt.close("all")


# %% 4. Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = Gestor_nova.MainWindow(root)

    def on_closing():
        cleanCanvas()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
