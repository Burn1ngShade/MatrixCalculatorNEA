import tkinter as tk
import constants as c
from graphic_matrix_calculation import Graphic_Matrix_Calculation
from matrix_window import Matrix_Window
from login_window import Login_Window
from visual_window import Visual_Window

class Matrix_Calculator:    
    def __init__(self, root):
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.root = root
        self.windows = [Login_Window(self), Matrix_Window(self), Visual_Window(self)]
        
        self.load_account("Guest")
        self.open_window(0)
        
    def open_window(self, index):        
        self.windows[index].panel.tkraise()
        root.geometry(c.WINDOW_GEOMETRY[index])

    def load_account(self, username):
        self.username = username
        self.windows[1].user_name.config(text=f"Logged In As [{username}]")
        
    def log_out(self):
        if (self.username != "Guest"): Graphic_Matrix_Calculation.save_matrix_calculations(self.username)
        Graphic_Matrix_Calculation.clear_matrix_calculations()
        self.load_account("Guest")
        
    def on_close(self):
        if (self.username != "Guest"): Graphic_Matrix_Calculation.save_matrix_calculations(self.username)
        self.root.destroy()
        
root = tk.Tk()
root.title("Matrix Calculator")
root.pack_propagate(0)
root.resizable(False, False)
root.geometry("800x800") #initally set as this so the window is placed nicely
root.iconbitmap("Assets/icon.ico")

Matrix_Calculator(root)

root.mainloop()
    
