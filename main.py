import tkinter as tk
from matrix_window import Matrix_Window
from login_window import Login_Window
from visual_window import Visual_Window

class Matrix_Calculator:    
    def __init__(self, root):
        self.root = root
        self.username = "Guest"
        self.windows = [Login_Window(self), Matrix_Window(self), Visual_Window(self)]
        self.open_window(1)
        
    def open_window(self, index):
        self.windows[index].panel.tkraise()

    def load_account(self, username):
        self.username = username
        self.windows[1].user_name.config(text=f"Logged In As [{username}]")
        
        

root = tk.Tk()
root.title("Matrix Calculator")
root.geometry("800x800")
root.pack_propagate(0)
root.resizable(False, False)
root.iconbitmap("Assets/icon.ico")

Matrix_Calculator(root)

root.mainloop()
    
