#%% 1. Head
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

#%% 2. Imports
from tkinter import messagebox
import customtkinter as ctk
import datetime
import json
import Gestor_nova

#%% 3. Code
def count_tasks(task_treeview, label_task, label_completed_task):
    number_tasks = len(task_treeview.get_children())
    completed_task = sum(1 for task in task_treeview.get_children() 
                        if task_treeview.item(task)["values"][2] == "Completada")

    label_task.configure(text = f"Tareas totales: {number_tasks}")
    label_completed_task.configure(text = f"Tareas completadas: {completed_task}")

def add_task(entry, list, task_treeview, label_task, label_completed_task):
    task = entry.get()
    priority = list.get()
    state = "Activa"
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if len(task) != 0: 
        insert = task_treeview.insert("", "end", values = [task, priority, state, date])
        count_tasks(task_treeview, label_task, label_completed_task)
        entry.delete(0, "end")
        return insert
    else:
        messagebox.showerror(title = "ERROR",message = "Error al introducir. El entry está vacío o incluye algún carácter no permitido.")
        return
  
def eliminate(task_treeview, label_task, label_completed_task):
    tasks = task_treeview.selection()
    if tasks:
        for task in tasks:
            task_treeview.delete(task)
        count_tasks(task_treeview, label_task, label_completed_task)
        messagebox.showinfo(title = "Deleted", message = "Fila/s eliminada/s correctamente.")
    else:
        messagebox.showwarning(title = "Warning", message = "Seleccione al menos una fila para eliminar.")

def import_from_json(task_treeview, label_task, label_completed_task):
    with open("examples.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)
        if tasks:
            for task in tasks:
                task_treeview.insert("", "end", values = [task["Tarea"], task["Prioridad"], task["Estado"], task["Fecha"]])
        count_tasks(task_treeview, label_task, label_completed_task)
                
def mark_as_completed(task_treeview, label_task, label_completed_task):
    tasks = task_treeview.selection()
    if tasks:
        for task in tasks:
            old_values = task_treeview.item(task, "values")
            task_treeview.item(task, values = (old_values[0], old_values[1], "Completada", old_values[3]))
        count_tasks(task_treeview, label_task, label_completed_task)
        

    else:
        messagebox.showwarning(title = "Warning", message = "Seleccione al menos una tarea para marcar como completada.")
        
def edit_tasks(event, task_treeview):
    task = task_treeview.selection()
    if task:
        ctkinput = ctk.CTkInputDialog(text = "Introduce el nuevo nombre")
        task_name = ctkinput.get_input()
        ctkinput2 = ctk.CTkInputDialog(text = "Introduce la prioridad (Alta, Media, Baja)")
        priority = ctkinput2.get_input()
        ctkinput3 = ctk.CTkInputDialog(text = "Introduce el estado de la tare (Activa o Completada)")
        state = ctkinput3.get_input()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if priority.strip() not in ["Alta", "Media", "Baja"]:
            messagebox.showwarning(title = "Warning", message= "Debes escribir un valor de prioridad correcto.")
            return
        elif state.strip() not in ["Activa", "Completada"]:
            messagebox.showwarning(title = "Warning", message= "Debes escribir un valor de estado correcto.")
            return
        else:
            task_treeview.item(task, values = (task_name, priority, state, date))
            messagebox.showinfo(title = "Info", message = "La fila ha sido editada correctamente")


def change_appearance_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")
 
#%% 4. Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = Gestor_nova.MainWindow(root)
    root.mainloop()