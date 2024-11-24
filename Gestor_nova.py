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
        self.root.grid_rowconfigure(3, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        treeview_style()
        notebook_style()
        
        self.frame_mid = FrameMid(self.root)
        self.frame_mid.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 20)

        self.frame_top = FrameTop(self.root, self.frame_mid.task_treeview)
        self.frame_top.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 20, pady = 10)

        self.menu = MenuTreeview(self.root, self.frame_mid.task_treeview, 
                                self.frame_top.task_label, self.frame_top.label_completed_task, self.frame_mid.notebook, self.frame_mid.tab2)
                
        self.frame_bot = FrameBot(self.root, self.frame_mid.task_treeview, self.frame_top.task_label,
                                self.frame_top.label_completed_task, self.frame_mid.notebook, self.menu, self.frame_mid.tab2)
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
        
        self.list = ctk.CTkComboBox(self, values = ["High", "Medium", "Low"], font = ("Helvetica",16),
                                    state = "readonly")
        self.list.grid(row = 0, column = 1 , sticky = tk.EW, padx = 30)
        
        self.add_button = ctk.CTkButton(self, text = "Add task", 
                                        command = lambda: Main.add_task(self.task_entry, self.list, task_treeview, 
                                                                        self.task_label, self.label_completed_task),
                                        corner_radius= 20, border_width = 2, 
                                        fg_color="transparent", font = ("Helvetica",16))
        self.add_button.grid(row = 0, column = 2, sticky = tk.EW, padx = 20)
        
        self.task_label = ctk.CTkLabel(self, text = "Total tasks: 0", font = ("Helvetica", 14))
        self.task_label.grid(row = 1, column = 0, sticky = tk.EW)

        self.label_completed_task = ctk.CTkLabel(self, text = "Completed tasks: 0", font = ("Helvetica", 14))
        self.label_completed_task.grid(row = 1, column = 2, sticky = tk.EW)


class FrameMid(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)       
        
        self.notebook = ttk.Notebook(self, style="Dark.TNotebook")
        self.notebook.grid(row=0, column=0, sticky=tk.NSEW)
        self.tab1 = ctk.CTkFrame(self.notebook)  
        self.tab2 = ctk.CTkFrame(self.notebook)  
        self.notebook.add(self.tab1, text="Task Manager")
        self.notebook.add(self.tab2, text="Gantt chart")
         
        self.tab1.grid_rowconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(0, weight=1)
         
        self.task_treeview = ttk.Treeview(self.tab1, columns = ["Task", "Priority", "State", "Date", "EndDate"],
                                         show = "headings", style="Dark.Treeview")
        self.task_treeview.heading("Task", text = "Task")
        self.task_treeview.heading("Priority", text = "Priority")
        self.task_treeview.heading("State", text = "State")
        self.task_treeview.heading("Date", text = "Date")
        self.task_treeview.heading("EndDate", text = "EndDate")
        self.task_treeview.grid(row = 0, column = 0, sticky = tk.NSEW)
        
        self.task_treeview.bind("<Double-1>", lambda event: Main.edit_tasks(event, self.task_treeview, self.winfo_toplevel()))     
 
        self.scroll = ttk.Scrollbar(self.tab1, orient="vertical")
        self.task_treeview.configure(yscroll = self.scroll.set)
        self.scroll.grid(row = 0, column = 1, sticky = tk.NS)
        
        self.tab2.grid_columnconfigure(0, weight = 1)
        self.tab2.grid_rowconfigure(0, weight = 1)
        self.tab2.grid_rowconfigure(1, weight = 10)
        
        self.button_gantt = ctk.CTkButton(self.tab2, text = "Generate Gantt", 
                         command = lambda: Main.generate_gantt(self.tab2, self.task_treeview))
        self.button_gantt.grid(row = 0, column = 0, sticky = tk.N)


class FrameBot(ctk.CTkFrame):
    def __init__(self, master, task_treeview, label_task, label_completed_task, notebook, menu_treeview, tab2):
        super().__init__(master)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure([0, 1, 2], weight = 1)

        self.button_eliminate = ctk.CTkButton(self, text = "Delete", 
                                            command = lambda: Main.delete(task_treeview, label_task, label_completed_task), 
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.button_eliminate.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 10)

        self.button_completed = ctk.CTkButton(self, text="Mark as completed", 
                                            command= lambda: Main.mark_as_completed(task_treeview, label_task, label_completed_task),
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.button_completed.grid(row = 0, column = 1, sticky = tk.NSEW, padx = 10)

        self.img = Image.open("Images\\light_dark.ico")
        self.img_resized = self.img.resize((30, 30))
        self.img = ImageTk.PhotoImage(self.img_resized)
        self.light_dark_button = ctk.CTkButton(self, text = "", 
                                            command = lambda: Main.change_appearance_mode(task_treeview, notebook, menu_treeview, tab2), 
                                            image= ctk.CTkImage(dark_image=self.img_resized, light_image=self.img_resized),
                                            fg_color="transparent", border_width = 2, corner_radius = 20)
        self.light_dark_button.grid(row = 0, column = 2, sticky = tk.NSEW, padx = 10)


class Toplevel(ctk.CTkToplevel):
    def __init__(self, master, current_values):
        super().__init__(master)

        center_window(self, 400)
        self.grid_rowconfigure([0, 1, 2, 3], weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.task_entry = ctk.CTkEntry(self, placeholder_text = "Insert new task name")
        self.task_entry.insert(0, current_values[0])
        self.task_entry.grid(row = 0, column = 0, sticky = tk.EW, padx = 50)

        self.priority = ctk.CTkComboBox(self, values=["High", "Medium", "Low"], state = "readonly")
        self.priority.set(current_values[1])
        self.priority.grid(row = 1, column = 0, sticky = tk.EW, padx = 50)

        self.state_entry = ctk.CTkEntry(self, placeholder_text = "Insert new task state")
        self.state_entry.insert(0, current_values[2]) 
        self.state_entry.grid(row = 2, column = 0, sticky = tk.EW, padx = 50)        

        self.button = ctk.CTkButton(self, text = "Confirm",
                                    command = self.store_data) 
        self.button.grid(row = 3, column = 0, sticky = tk.EW, padx = 70)

        self.result = None
    def store_data(self):
        self.result = {
            "task_name": self.task_entry.get(),
            "priority": self.priority.get(),
            "state": self.state_entry.get()
        }
        self.destroy()


class MenuTreeview(tk.Menu):
    def __init__(self, master, task_treeview, label_task, label_completed_task, notebook, tab2):
        super().__init__(master)
        master.configure(menu = self)
       
        self.right_click_menu = tk.Menu(self, tearoff=0)
        self.right_click_menu.add_command(
            label="Edit Task",
            command=lambda: Main.edit_tasks(None, task_treeview, self.master)
        )
        self.right_click_menu.add_command(
            label="Delete Task",
            command=lambda: Main.delete(task_treeview, label_task, label_completed_task)
        )
        self.right_click_menu.add_command(
            label="Mark Task Completed",
            command=lambda: Main.mark_as_completed(task_treeview, label_task, label_completed_task)
        )
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(
            label="Toggle Theme",
            command= lambda: Main.change_appearance_mode(task_treeview, notebook, self, tab2)
        )

        self.menu_styles = right_click_menu_style()
        self.current_theme = "dark_theme" 
        self.apply_theme(self.current_theme)

        self.master.bind("<Button-3>", self.show_right_click_menu)

    def apply_theme(self, theme):
        theme = self.menu_styles[theme]
        self.right_click_menu.config(
            bg=theme["bg"],
            fg=theme["fg"],
            activebackground=theme["activebackground"],
            activeforeground=theme["activeforeground"]
        )

    def toggle_theme(self):
        self.current_theme = "light_theme" if self.current_theme == "dark_theme" else "dark_theme"
        self.apply_theme(self.current_theme)

    def show_right_click_menu(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)



def treeview_style():
    # Dark mode
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.Treeview",
                    background="#1e1e1e",  
                    foreground="white",  
                    fieldbackground="#1e1e1e",  
                    bordercolor="#3e3e3e",  
                    borderwidth=1)
    style.configure("Dark.Treeview.Heading",
                    background="#3e3e3e",  
                    foreground="white",  
                    relief="flat")
    style.map("Dark.Treeview.Heading",
              background=[("active", "#575757")], 
              relief=[("pressed", "groove"), ("active", "raised")])
    # Light mode
    style.configure("Light.Treeview",
                    background="#ffffff",  
                    foreground="black",   
                    fieldbackground="#ffffff", 
                    bordercolor="#d9d9d9", 
                    borderwidth=1)
    style.configure("Light.Treeview.Heading",
                    background="#f0f0f0",  
                    foreground="black",   
                    relief="flat")
    style.map("Light.Treeview.Heading",
              background=[("active", "#e0e0e0")],
              relief=[("pressed", "groove"), ("active", "raised")])


def notebook_style():
    # Dark mode for notebook
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.TNotebook", background="black", borderwidth=0)
    style.configure("Dark.TNotebook.Tab", background="gray20", foreground="white", padding=(10, 5))
    style.map("Dark.TNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "white")])
    # Light mode for notebook
    style.configure("Light.TNotebook", background="white", borderwidth=0)
    style.configure("Light.TNotebook.Tab", background="lightgray", foreground="black", padding=(10, 5))
    style.map("Light.TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "black")])

def right_click_menu_style():
    # Theme for right click menu
    return{
        "dark_theme": {
            "bg": "#1e1e1e",
            "fg": "white",
            "activebackground": "#4A6984",
            "activeforeground": "white", 
            "borderwidth": 1,
        },
        "light_theme": {
            "bg": "white",
            "fg": "black",
            "activebackground": "#e0e0e0",
            "activeforeground": "black",
            "borderwidth": 1,
            "relief": "solid"
        }
    }