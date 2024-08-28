import tkinter as tk

class Window(): # base abstract class for windows to inherit from    
    def __init__(self, app, font_size = 12):
        self.app = app
        self.panel = tk.Frame(app.root, bg="snow3")
        self.panel.option_add("*font", f"Consolas {font_size}")
        self.panel.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.setup_window()
    
    def setup_window(self): pass # called on window creation, to render and setup window 
        