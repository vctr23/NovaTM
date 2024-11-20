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

    if len(task) != 0:
        insert = task_treeview.insert(
            "", "end", values=[task, priority, state, date])
        count_tasks(task_treeview, label_task, label_completed_task)
        entry.delete(0, "end")
        return insert
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
                task_treeview.insert("", "end", values=[
                                     task["Task"], task["Priority"], task["State"], task["Date"], task["EndDate"]])
        count_tasks(task_treeview, label_task, label_completed_task)


def mark_as_completed(task_treeview, label_task, label_completed_task):
    tasks = task_treeview.selection()
    if tasks:
        for task in tasks:
            old_values = task_treeview.item(task, "values")
            task_treeview.item(task, values=(
                old_values[0], old_values[1], "Completed", old_values[3]))
        count_tasks(task_treeview, label_task, label_completed_task)

    else:
        messagebox.showwarning(
            title="Warning", message="Select at least one task to mark as completed.")


def edit_tasks(event, task_treeview):
    task = task_treeview.selection()
    if task:
        ctkinput = ctk.CTkInputDialog(text="Introduce the new task name:")
        task_name = ctkinput.get_input()
        ctkinput2 = ctk.CTkInputDialog(
            text="Introduce task priority (High, Medium, Low):")
        priority = ctkinput2.get_input()
        ctkinput3 = ctk.CTkInputDialog(
            text="Introduce task state (Active, Completed):")
        state = ctkinput3.get_input()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if priority.strip() not in ["High", "Medium", "Low"]:
            messagebox.showwarning(
                title="Warning", message="Write a correct priority value.")
            return
        elif state.strip() not in ["Active", "Completed"]:
            messagebox.showwarning(
                title="Warning", message="Write a correct state value.")
            return
        else:
            task_treeview.item(task, values=(task_name, priority, state, date))
            messagebox.showinfo(
                title="Info", message="Row editted succesfully")


def change_appearance_mode(task_treeview, notebook):
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        task_treeview["style"] = "Light.Treeview"
        notebook["style"] = "Light.TNotebook"
    else:
        ctk.set_appearance_mode("Dark")
        task_treeview["style"] = "Dark.Treeview"
        notebook["style"] = "Dark.TNotebook"


def generate_gantt(tab2, task_treeview):
    tasks = []
    start_dates = []
    end_dates = []

    for item in task_treeview.get_children():
        task, priority, sdate, sdate, edate = task_treeview.item(item)[
            "values"]
        start_date = pd.to_datetime(sdate)
        end_date = pd.to_datetime(edate)
        tasks.append(task)
        start_dates.append(pd.to_datetime(start_date))
        end_dates.append(pd.to_datetime(end_date))

    start_dates = pd.to_datetime(start_dates)
    end_dates = pd.to_datetime(end_dates)

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.barh(tasks, (end_dates - start_dates), left=start_dates)

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    plt.title("Diagrama de Gantt")
    plt.xlabel("Fecha")
    plt.ylabel("Tareas")

    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.NSEW)


# %% 4. Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = Gestor_nova.MainWindow(root)
    root.mainloop()
