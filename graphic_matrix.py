import tkinter as tk
import constants as c   
from data_handler import Data_Handler
from matrix import Matrix

# same as matrix class, but the ability to be rendered
class Graphic_Matrix(Matrix):
    def __init__(self, width, height, reflect, panel, master):
        super().__init__(width, height) # base matrix init
        
        self.vcmd = (master.register(lambda P, W: Data_Handler.validate_matrix_input(P, W, self))) # must be put here as a validation updates the needed matrix
        self.reflect = reflect # should we reflect the matrix to the right hand side of the screen
        self.panel = panel
        self.content_entrys = [] # the entry boxes to input matrix contents
        
        self.setup_graphic_matrix()
        
    def setup_graphic_matrix(self):
        self.modification_buttons = [
            tk.Button(self.panel, text="+", width=1, height=1, command=lambda: (self.set_dimensions(self.width + 1, self.height), self.draw_to_panel())), # increase width
            tk.Button(self.panel, text="+", width=1, height=1, command=lambda: (self.set_dimensions(self.width - 1, self.height), self.draw_to_panel())), # decrease width
            tk.Button(self.panel, text="+", width=1, height=1, command=lambda: (self.set_dimensions(self.width, self.height + 1), self.draw_to_panel())), # increase height
            tk.Button(self.panel, text="+", width=1, height=1, command=lambda: (self.set_dimensions(self.width, self.height - 1), self.draw_to_panel())), # decrease height
            tk.Button(self.panel, text="c", width = 1, height = 1, command=lambda: (self.refresh(True), self.draw_to_panel())) # clear matrix contents
        ]
        
    # --- RENDERING FUNCTIONS ---
     
    def draw_to_panel(self): #draw matrix to panel
        self.clear_from_panel() # we dont want to double stack so lets first clear whatever we have currently
        self.panel.option_add("*font", "Consolas 8") # update current font size
        
        x_base = c.MATRIX_REFLECTED_X_BASE if self.reflect == -1 else c.MATRIX_X_BASE
    
        # ensure that the matrix is centered
        x_offset = x_base - 40 * (self.width - 1) 
        y_offset = c.MATRIX_Y_BASE - 15 * (self.height - 1)
         
        for x in range(self.width):
            self.content_entrys.append([])
            for y in range(self.height):
                self.content_entrys[x].append(tk.Entry(self.panel, name=f"entry {x + y * self.width} [{self.reflect}]", validate='key', validatecommand=(self.vcmd, "%P", "%W"), width=10))
                self.content_entrys[x][y].place(x = x * 80 + x_offset, y = y * 30 + y_offset, anchor="center")
                
                if (self.content[x][y] != 0): # QOL so you dont have to backspace zeros everytime you want to use a matrix 
                    self.content_entrys[x][y].insert(0, f"{self.content[x][y]:g}")
                
        # redraw buttons surrounding newly sized and placed matrix
        self.modification_buttons[0].place(x = x_base - 15, y = y_offset + self.height * 30, anchor="center")
        self.modification_buttons[1].place(x = x_base + 15, y = y_offset + self.height * 30, anchor="center")
        self.modification_buttons[2].place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE - 37, anchor="center")
        self.modification_buttons[3].place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE, anchor="center")
        self.modification_buttons[4].place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE + 37, anchor="center")
        
    def clear_from_panel(self): # clears the matrix from it's panel
        for x in range(len(self.content_entrys)): 
            for y in range(len(self.content_entrys[x])):
                self.content_entrys[x][y].destroy()
                
        self.content_entrys = []