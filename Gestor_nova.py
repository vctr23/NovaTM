#%% 1. Head
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

#%%  2. Imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import Main
#%% 3. Code
def center_window(root, window_width):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_height = int((screen_height * window_width)/screen_width)
    
    x_pos = int(screen_width/2 - window_width/2)
    y_pos = int(screen_height/2 - window_height/2)
    
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
#%% 4. Classes
class MainWindow():
    """
    Clase que contiene el root y sus atributos
    
    Return -> None.
    """
    def __init__(self, root):
        ctk.set_default_color_theme("green")
        self.root = root
        self.root.title("NovaTM")
        center_window(self.root, 1100)
        
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 10)
        self.root.grid_rowconfigure(2, weight = 1)
        self.root.columnconfigure(0, weight = 1)
              
        self.frame_mid = FrameMid(self.root)
        self.frame_mid.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 20)

        self.frame_top = FrameTop(self.root, self.frame_mid.task_treeview)
        self.frame_top.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 20, pady = 10)
                
        self.frame_bot = FrameBot(self.root, self.frame_mid.task_treeview, self.frame_top.task_label,
                                self.frame_top.label_completed_task)
        self.frame_bot.grid(row = 2, column = 0, sticky = tk.NSEW, padx = 20, pady = 10)
        
        self.upload = Main.import_from_json(self.frame_mid.task_treeview, self.frame_top.task_label,
                                            self.frame_top.label_completed_task)
    
        
class FrameTop(ctk.CTkFrame):
    def __init__(self, master, task_treeview):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure([0, 1, 2], weight = 1)
     
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Insert task name", font = ("Helvetica", 16))
        self.task_entry.grid(row = 0,column = 0, sticky = tk.EW, padx = 20)
        
        self.list = ctk.CTkComboBox(self, values = ["Alta", "Media", "Baja"], font = ("Helvetica",16))
        self.list.grid(row = 0, column = 1 , sticky = tk.EW, padx = 30)
        
        self.add_button = ctk.CTkButton(self, text = "Add task", 
                                        command = lambda: Main.add_task(self.task_entry, self.list, task_treeview, self.task_label, 
                                                                        self.label_completed_task),
                                        corner_radius= 20, border_width = 2, 
                                        fg_color="transparent", font = ("Helvetica",16))
        self.add_button.grid(row = 0, column = 2, sticky = tk.EW, padx = 20)
        
        self.task_label = ctk.CTkLabel(self, text = "Tareas totales: 0", font = ("Helvetica", 14))
        self.task_label.grid(row = 1, column = 0, sticky = tk.EW)

        self.label_completed_task = ctk.CTkLabel(self, text = "Tareas completadas: 0", font = ("Helvetica", 14))
        self.label_completed_task.grid(row = 1, column = 2, sticky = tk.EW)

class FrameMid(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.task_treeview = ttk.Treeview(self, columns = ["Tarea", "Prioridad", "Estado", "Fecha"], show = "headings")
        self.task_treeview.heading("Tarea", text = "Tarea")
        self.task_treeview.heading("Prioridad", text = "Prioridad")
        self.task_treeview.heading("Estado", text = "Estado")
        self.task_treeview.heading("Fecha", text = "Fecha")
        self.task_treeview.grid(row = 0, column = 0, sticky = tk.NSEW)
        
        self.task_treeview.bind("<Double-1>", lambda event: Main.edit_tasks(event, self.task_treeview))     
        # See if the scrollbar works:
        # contacts = []
        # for n in range(1, 100):
        #     contacts.append((f'first {n}', f'Alta {n}', f'Activo', datetime.datetime.now()))

        # for contact in contacts:
        #     self.task_treeview.insert('', tk.END, values=contact)

        self.scroll = ttk.Scrollbar(self, orient="vertical", command = self.task_treeview.yview)
        self.task_treeview.configure(yscroll = self.scroll.set)
        self.scroll.grid(row = 0, column = 1, sticky = tk.NS)
        
class FrameBot(ctk.CTkFrame):
    def __init__(self, master, task_treeview, label_task, label_completed_task):
        super().__init__(master)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure([0, 1, 2], weight = 1)

        self.button_eliminate = ctk.CTkButton(self, text = "Eliminar", command = lambda: Main.eliminate(task_treeview, label_task, label_completed_task), 
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.button_eliminate.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 10)

        self.button_completed = ctk.CTkButton(self, text="Mark as completed", 
                                            command= lambda: Main.mark_as_completed(task_treeview, label_task, label_completed_task),
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.button_completed.grid(row = 0, column = 1, sticky = tk.NSEW, padx = 10)

        self.img = Image.open("Images\\light_dark.ico")
        self.img_resized = self.img.resize((30, 30))
        self.img = ImageTk.PhotoImage(self.img_resized)
        self.light_dark_button = ctk.CTkButton(self, text = "", command = lambda: Main.change_appearance_mode(),
                                            image= ctk.CTkImage(dark_image=self.img_resized, light_image=self.img_resized),
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.light_dark_button.grid(row = 0, column = 2, sticky = tk.NSEW, padx = 10)