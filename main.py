import tkinter as tk
import constants as c
from graphic_matrix_calculation import Graphic_Matrix_Calculation
from matrix_window import Matrix_Window
from login_window import Login_Window
from visual_window import Visual_Window

class Matrix_Calculator: # primary class handling windows and accounts, aswell as being the root of the whole app 
    def __init__(self, root):
        root.protocol("WM_DELETE_WINDOW", self.on_close) # extra stuff to do when closing app
        
        self.root = root
        self.windows = [Login_Window(self), Matrix_Window(self), Visual_Window(self)]
        
        self.load_account(c.GUEST_USERNAME) 
        self.open_window(1)
        
    def open_window(self, index): # display given index window 
        self.windows[index].panel.tkraise()
        root.geometry(c.WINDOW_GEOMETRY[index])

    # --- ACCOUNT FUNCTIONS ---

    def load_account(self, username): # load account with given username
        self.username = username
        self.windows[1].user_name.config(text=f"Logged In As [{username}]")
        if (self.username != c.GUEST_USERNAME): Graphic_Matrix_Calculation.load_matrix_calculations(self.username)
        
    def log_out(self): # log out of currently logged account
        if (self.username != c.GUEST_USERNAME): Graphic_Matrix_Calculation.save_matrix_calculations(self.username)
        Graphic_Matrix_Calculation.clear_matrix_calculations()
        self.load_account(c.GUEST_USERNAME)
        
    def on_close(self): # called on application close by (alt f4 or manual close)
        if (self.username != c.GUEST_USERNAME): Graphic_Matrix_Calculation.save_matrix_calculations(self.username)
        self.root.destroy()

# --- PROJECT INITIALISATION ---

root = tk.Tk()
root.title("Matrix Calculator")
root.resizable(False, False)
root.geometry(c.WINDOW_GEOMETRY[1]) #initally set as this so the window is placed nicely
root.iconbitmap("Assets/icon.ico")

Matrix_Calculator(root) # create instance of the app
root.mainloop()
    
 