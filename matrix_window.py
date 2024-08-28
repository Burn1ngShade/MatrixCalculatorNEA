import tkinter as tk
from tkinter import ttk 
import constants as c
from matrix import Matrix
from graphic_matrix import Graphic_Matrix
from graphic_matrix_calculation import Graphic_Matrix_Calculation as gmc
from data_handler import Data_Handler
from window import Window

# main window for matrices
class Matrix_Window(Window):
    def __init__(self, app):
        super().__init__(app, 8)
        
    def setup_window(self): # initalises and draws window on startup
        tk.Frame(self.panel, bg="gainsboro", height=304).pack(side=tk.TOP, fill=tk.X)
        
        self.setup_transformation_buttons()
        self.setup_login_buttons()
        self.setup_previous_calculations()
        self.setup_matrice()
        
    def setup_login_buttons(self): # draw login stuff
        self.user_name_label = tk.Label(self.panel, text="LOG IN TEST", bg = "gainsboro")
        self.user_name_label.place(x = 400,  y= 235, anchor="center")
        tk.Button(self.panel, text="Log Out", width = 8, height = 1, command=lambda:
            (self.app.open_window(0), self.app.log_out())).place(x = 400, y = 260, anchor="center")
        
    def setup_matrice(self): # create and render matrice
        self.mat = [Graphic_Matrix(2, 2, 1, self.panel, self.app.root), Graphic_Matrix(2, 2, -1, self.panel, self.app.root)]
        self.mat[0].draw()
        self.mat[1].draw()
        
    def setup_transformation_buttons(self): # draw matrix buttons        
        #double matrice buttons
        tk.Button(self.panel, text="<->", width=7, height=1, command=lambda: #swap matrix button 
            (Matrix.swap_matrice(self.mat[0], self.mat[1]), self.mat[0].draw(), self.mat[1].draw())).place(
            x = 400, y = c.MATRIX_Y_BASE - 45, anchor="center")
        tk.Button(self.panel, text="A x B", width=7, height=1, command=lambda: #multiply button
            (gmc.log_gmc([("", self.mat[0]), ("x", self.mat[1]), ("=", Matrix.multiply_matrice(self.mat[0], self.mat[1]))]))).place(
            x = 400, y = c.MATRIX_Y_BASE - 15, anchor="center")
        tk.Button(self.panel, text="A + B", width=7, height=1, command=lambda: #add button
            (gmc.log_gmc([("", self.mat[0]), ("+", self.mat[1]), ("=", Matrix.add_sub_matrice(self.mat[0], self.mat[1]))]))).place(
            x = 400, y = c.MATRIX_Y_BASE + 15, anchor="center")
        tk.Button(self.panel, text="A - B", width=7, height=1, command=lambda: #subtract button
            (gmc.log_gmc([("", self.mat[0]), ("-", self.mat[1]), ("=", Matrix.add_sub_matrice(self.mat[0], self.mat[1], True))]))).place(
            x = 400, y = c.MATRIX_Y_BASE + 45, anchor = "center")
            
        #single matrix buttons
        self.button_entrys = []
        
        for i in range(2): # multiply by scalar button
            self.button_entrys.append(tk.Entry(self.panel, validate="key", validatecommand=self.app.validate_float, width=4))
            self.button_entrys[i].insert(0, "2")
            self.button_entrys[i].place(x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + 42 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y, anchor="center")
            
            tk.Button(self.panel, text="Multiply By", width=12, height=1, command=lambda i=i:
                (gmc.log_gmc([(f"{self.button_entrys[i].get()} x", self.mat[i]), ("=", self.mat[i].scalar_multiply(float(self.button_entrys[i].get())))]))).place(
                    x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING - 15 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y, anchor="center")
        
        for i in range(2): # to the power of button
            self.button_entrys.append(tk.Entry(self.panel, validate="key", validatecommand=self.app.validate_int, width=4))
            self.button_entrys[i + 2].insert(0, "2")
            self.button_entrys[i + 2].place(x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + 42 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor = "center")
            
            tk.Button(self.panel, text="Raised By", width=12, height=1, command=lambda i=i:
                (gmc.log_gmc([("", self.mat[i]), (f"^({self.button_entrys[i + 2].get()}) =", self.mat[i].to_pow(float(self.button_entrys[i + 2].get())))]))).place(
                    x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING - 15 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor="center")
                
        for i in range(2): 
            # determinant buttons
            tk.Button(self.panel, text = "Determinant", width=17, height=1, command=lambda i=i:
            (gmc.log_gmc([("Det", self.mat[i], f"= {self.mat[i].det():g}" if not isinstance(self.mat[i].det(), bool) else False)]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 66, anchor="center")      

            # invert buttons
            tk.Button(self.panel, text="Invert", width=17, height=1, command=lambda i=i:
            (gmc.log_gmc([("", self.mat[i]), ("^(-1) =", self.mat[i].invert())]))).place(    
                x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 66, anchor="center")

            # tranpose buttons
            tk.Button(self.panel, text = "Transpose", width=17, height=1, command=lambda i=i:
            (gmc.log_gmc([("Transpose", self.mat[i]), ("=", self.mat[i].transpose())]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor="center")
            
            tk.Button(self.panel, text="Visualise", width=17, height=1, command=lambda i=i:
            (self.app.windows[2].visualise_matrix(self.mat[i]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y, anchor="center")
            
            tk.Button(self.panel, text="Rank", width=17, height=1, command=lambda i=i:
            (gmc.log_gmc([("Rank", self.mat[i], f"= {self.mat[i].rank():g}")]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y + 99, anchor="center")
            
            tk.Button(self.panel, text="Row Echelon Form", width=17, height=1, command=lambda i=i:
             (gmc.log_gmc([("", self.mat[i]), ("~", Matrix.row_echelon_form(self.mat[i]))]))).place(
                x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y + 99, anchor="center")
             
    def setup_previous_calculations(self): # draws previous matrix calculations
        self.prev_trans_text = tk.Label(self.panel, font=("Consolas", 12), text="Previous Matrix Calculations --- Page [1 / 1]", bg = "gainsboro")
        self.prev_trans_text.place(x = 10,  y= 326, anchor="w")        
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", font=("Consolas", 12), fieldbackground="gainsboro", background="gainsboro", foreground="black", arrowcolor="black")
        
        self.sort_gmc_dd = ttk.Combobox(self.panel, width=28, font=("Consolas", 12), state='readonly', values= c.MATRIX_CALC_SORT_OPTIONS)
        self.sort_gmc_dd.set("Creation Date (Descending)")
        self.sort_gmc_dd.place(x = 790, y = 326, anchor="e")
        self.sort_gmc_dd.bind("<<ComboboxSelected>>", lambda event: gmc.on_sort_method_select(event, self.sort_gmc_dd))
        
        tk.Frame(self.panel, bg="gainsboro", height=31, width=44).place(x = 450, y=326, anchor="center")
        
        tk.Button(self.panel, text="<", width=1, height=1, command=lambda:
            (gmc.update_gmc_page(gmc.current_page - 1))).place(x = 440, y = 326, anchor="center")
        tk.Button(self.panel, text=">", width=1, height=1, command=lambda:
            gmc.update_gmc_page(gmc.current_page + 1)).place(x = 460, y = 326, anchor="center")