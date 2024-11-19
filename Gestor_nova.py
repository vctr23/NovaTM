#%% 1. Encabezado
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:14:03 2024

@author: vctr23
"""

#%%  2. Imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
#%% 3. Código
def center_window(root, window_width):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_height = int((screen_height * window_width)/screen_width)
    
    x_pos = int(screen_width/2 - window_width/2)
    y_pos = int(screen_height/2 - window_height/2)
    
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
#%% 4. Clases
class MainWindow():
    """
    Clase que contiene el root y sus atributos
    
    Return -> None.
    """
    def __init__(self, root):
        ctk.set_appearance_mode("system")
        self.root = root
        self.root.title("NovaTM")
        center_window(self.root, 1200)
        
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 3)
        self.root.grid_rowconfigure(2, weight = 1)
        self.root.columnconfigure(0, weight = 1)
        
        self.frame_top = FrameTop(self.root)
        self.frame_top.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 20, pady = 10)
        
                
        self.frame_mid = FrameMid(self.root)
        self.frame_mid.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 20)
        
                
        self.frame_bot = FrameBot(self.root)
        self.frame_bot.grid(row = 2, column = 0, sticky = tk.NSEW, padx = 20, pady = 10)
        
        
class FrameTop(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure([0, 1, 2], weight = 1)
     
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Insert task name", font = ("Helvetica", 16))
        self.task_entry.grid(row = 0,column = 0, sticky = tk.NSEW, padx = 20, pady = 20)
        
        self.list = ctk.CTkComboBox(self, values = ["Alta", "Media", "Baja"], font = ("Helvetica",16))
        self.list.grid(row = 0, column = 1 , sticky = tk.NSEW, padx = 30, pady = 20)
        
        self.add_button = ctk.CTkButton(self, text = "Add task", corner_radius= 20, border_width = 2, 
                                        fg_color="transparent", font = ("Helvetica",16), hover_color="#3A3434")
        self.add_button.grid(row = 0, column = 2, sticky = tk.NSEW, padx = 20, pady = 20)
        
        
class FrameMid(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        
class FrameBot(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
#%% Main
if __name__ == "__main__":
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()
    
        
    
    