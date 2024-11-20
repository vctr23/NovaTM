#%% 1. Head
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

#%% 2. Imports
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import datetime
import Gestor_nova

#%% 3. Code
counter = 0
def add_task(entry, list, task_treeview, label_task):
    global counter
    task = entry.get()
    priority = list.get()
    state = "Activo"
    date = datetime.datetime.now()

    if task.isalnum() and len(task) != 0:
        counter = counter + 1
        entry.delete(0, "end")
        insert = task_treeview.insert('', tk.END, values = [task, priority, state, date])
        label_task.configure(text = f"Tareas: {counter}")
        return insert
    else:
        # Show error message when entry is empty
        messagebox.showerror(title = "ERROR",message = "Error al introducir. El entry está vacío")
        return
  
def eliminate(task_treeview):
    obj = task_treeview.selection()[0]
    task_treeview.delete(obj)
    if not task_treeview.exists(obj):
        messagebox.showinfo(title = "Deleted", message = "Fila eliminada correctamente")
    else:
        return


    
    


#%% 4. Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = Gestor_nova.MainWindow(root)
    root.mainloop()