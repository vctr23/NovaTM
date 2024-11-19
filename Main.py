#%% 1. Head
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

#%% 2. Imports
import tkinter as tk
import customtkinter as ctk
import datetime
import Gestor_nova

#%% 3. Code
def add_task(entry, list, task_treeview):
    task = entry.get()
    priority = list.get()
    state = "Activo"
    date = datetime.datetime.now()

    insert = task_treeview.insert('', tk.END, values = [task, state, priority, date])

    return insert





#%% 4. Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = Gestor_nova.MainWindow(root)
    root.mainloop()