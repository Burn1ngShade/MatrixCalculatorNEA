import tkinter as tk
import entry_validation
import constants as c   
from matrix import Matrix

#base class for matrix graphical representation
class Graphic_Matrix(Matrix):
    def __init__(self, width, height, reflect, panel, master):
        super().__init__(width, height)
        
        self.vcmd = (master.register(lambda P, W: entry_validation.validate_mat_input(P, W, self)))
        
        self.reflect = reflect
        self.panel = panel
        self.content_entry = []
        
        self.incr_width = tk.Button(self.panel, text="+", width = 1, height = 1, command=lambda: (self.set_width(self.width + 1), self.draw()))
        self.decr_width = tk.Button(self.panel, text="-", width = 1, height = 1, command=lambda: (self.set_width(self.width - 1), self.draw()))
        self.incr_height = tk.Button(self.panel, text="+", width = 1, height = 1, command=lambda: (self.set_height(self.height + 1), self.draw()))
        self.decr_height = tk.Button(self.panel, text="-", width = 1, height = 1, command=lambda: (self.set_height(self.height - 1), self.draw()))
        self.clear = tk.Button(self.panel, text="c", width = 1, height = 1, command=lambda:(self.set(0, True), self.draw()))
        
    def draw(self): #draw matrix to window
        self.undraw()
        
        x_base = c.MATRIX_REFLECTED_X_BASE if self.reflect == -1 else c.MATRIX_X_BASE
    
        x_offset = x_base - 40 * (self.width - 1)
        y_offset = c.MATRIX_Y_BASE - 15 * (self.height - 1)
        
        for x in range(self.width):
            self.content_entry.append([])
            for y in range(self.height):
                self.content_entry[x].append(tk.Entry(self.panel, name=f"entry {x + y * self.width} [{self.reflect}]", validate='key', validatecommand=(self.vcmd, "%P", "%W"), width=10))
                self.content_entry[x][y].place(x = x * 80 + x_offset, y = y * 30 + y_offset, anchor="center")
                if (self.content[x][y] != 0): self.content_entry[x][y].insert(0, f"{self.content[x][y]:g}")
                
        # size modifiers
        self.incr_width.place(x = x_base - 15, y = y_offset + self.height * 30, anchor="center")
        self.decr_width.place(x = x_base + 15, y = y_offset + self.height * 30, anchor="center")
        self.incr_height.place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE - 37, anchor="center")
        self.decr_height.place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE, anchor="center")
        self.clear.place(x = x_base + (10 + 40 * (self.width)) * self.reflect, y = c.MATRIX_Y_BASE + 37, anchor="center")
        
    def undraw(self): #undraw the matrix from window
        for x in range(len(self.content_entry)):
            for y in range(len(self.content_entry[x])):
                self.content_entry[x][y].destroy()
                
        self.content_entry = []