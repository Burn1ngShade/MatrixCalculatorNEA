import tkinter as tk
from tkinter import ttk 
import constants as c
from matrix import Matrix
from graphic_matrix import Graphic_Matrix
from graphic_matrix_calculation import Graphic_Matrix_Calculation as GMC
import entry_validation

# main window for matrices
class Matrix_Window:
    def __init__(self, app):
        GMC.target_window = self
        
        self.app = app
        
        self.panel = tk.Frame(app.root, bg="snow3", height=800, width=800)
        self.panel.option_add( "*font", "Consolas 8" )
        self.panel.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        Matrix_Window.vcmd = app.root.register(entry_validation.validate_input), "%P"
        Matrix_Window.vcmd_int = app.root.register(entry_validation.validate_int_input), "%P"
        
        # ui seperators
        
        top_frame = tk.Frame(self.panel, bg="gainsboro", height=304)
        top_frame.pack(side=tk.TOP, fill=tk.X)  # Pack the frame at the top and fill horizontally
        
        # gmc options
        self.prev_trans_text = tk.Label(self.panel, font=("Consolas", 12), text="Previous Matrix Calculations --- Page [1 / 1]", bg = "gainsboro")
        self.prev_trans_text.place(x = 10,  y= 326, anchor="w")        
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", font=("Consolas", 12), fieldbackground="gainsboro", background="gainsboro", foreground="black", arrowcolor="black")
        
        self.sort_gmc_dd = ttk.Combobox(self.panel, width=28, font=("Consolas", 12), state='readonly', values= c.MATRIX_CALC_SORT_OPTIONS)
        self.sort_gmc_dd.set("Creation Date (Descending)")
        self.sort_gmc_dd.place(x = 790, y = 326, anchor="e")
        self.sort_gmc_dd.bind("<<ComboboxSelected>>", lambda event: GMC.on_sort_method_select(event, self.sort_gmc_dd))
        
        tk.Frame(self.panel, bg="gainsboro", height=31, width=44).place(x = 450, y=326, anchor="center")
        
        tk.Button(self.panel, text="<", width=1, height=1, command=lambda:
            (GMC.update_gmc_page(GMC.current_page - 1))).place(x = 440, y = 326, anchor="center")
        tk.Button(self.panel, text=">", width=1, height=1, command=lambda:
            GMC.update_gmc_page(GMC.current_page + 1)).place(x = 460, y = 326, anchor="center")

        # login data

        self.user_name = tk.Label(self.panel, text="LOG IN TEXST", bg = "gainsboro")
        self.user_name.place(x = 400,  y= 235, anchor="center")
        log_out = tk.Button(self.panel, text="Log Out", width = 8, height = 1, command=lambda:
            (self.app.open_window(0), self.app.log_out()))
        log_out.place(x = 400, y = 260, anchor="center")
        
        # define matrix
        
        self.mat_a = Graphic_Matrix(2, 2, 1, self.panel, app.root) #define left matrix 
        self.mat_b = Graphic_Matrix(2, 2, -1, self.panel, app.root) #define right matrix 
        self.mat = [self.mat_a, self.mat_b]
        
        self.mat_a.draw()
        self.mat_b.draw()
        
        # matrix customisation buttons
        
        self.matrix_transformation_buttons()
        
    # MATRIX TRANSFORMATIONS
    def matrix_transformation_buttons(self):
        #double matrice buttons
        tk.Button(self.panel, text="<->", width=7, height=1, command=lambda: #swap matrix button 
            (Matrix.swap_matrice(self.mat_a, self.mat_b), self.mat_a.draw(), self.mat_b.draw())).place(
            x = 400, y = c.MATRIX_Y_BASE - 45, anchor="center")
        tk.Button(self.panel, text="A x B", width=7, height=1, command=lambda: #multiply button
            (GMC.log_gmc([("", self.mat_a), ("x", self.mat_b), ("=", Matrix.multiply_matrice(self.mat_a, self.mat_b))]))).place(
            x = 400, y = c.MATRIX_Y_BASE - 15, anchor="center")
        tk.Button(self.panel, text="A + B", width=7, height=1, command=lambda: #add button
            (GMC.log_gmc([("", self.mat_a), ("+", self.mat_b), ("=", Matrix.add_sub_matrice(self.mat_a, self.mat_b))]))).place(
            x = 400, y = c.MATRIX_Y_BASE + 15, anchor="center")
        tk.Button(self.panel, text="A - B", width=7, height=1, command=lambda: #subtract button
            (GMC.log_gmc([("", self.mat_a), ("-", self.mat_b), ("=", Matrix.add_sub_matrice(self.mat_a, self.mat_b, True))]))).place(
            x = 400, y = c.MATRIX_Y_BASE + 45, anchor = "center")
            
        #single matrix buttons
        self.button_entrys = []
        
        for i in range(2): # multiply by scalar button
            self.button_entrys.append(tk.Entry(self.panel, validate="key", validatecommand=Matrix_Window.vcmd, width=4))
            self.button_entrys[i].insert(0, "2")
            self.button_entrys[i].place(x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + 42 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y, anchor="center")
            
            tk.Button(self.panel, text="Multiply By", width=12, height=1, command=lambda i=i:
                (GMC.log_gmc([(f"{self.button_entrys[i].get()} x", self.mat[i]), ("=", self.mat[i].scalar_multiply(float(self.button_entrys[i].get())))]))).place(
                    x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING - 15 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y, anchor="center")
        
        for i in range(2): # to the power of button
            self.button_entrys.append(tk.Entry(self.panel, validate="key", validatecommand=Matrix_Window.vcmd_int, width=4))
            self.button_entrys[i + 2].insert(0, "2")
            self.button_entrys[i + 2].place(x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + 42 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor = "center")
            
            tk.Button(self.panel, text="Raised By", width=12, height=1, command=lambda i=i:
                (GMC.log_gmc([("", self.mat[i]), (f"^({self.button_entrys[i + 2].get()}) =", self.mat[i].to_pow(float(self.button_entrys[i + 2].get())))]))).place(
                    x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING - 15 + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor="center")
                
        for i in range(2): # determinant buttons
            tk.Button(self.panel, text = "Determinant", width=17, height=1, command=lambda i=i:
            (GMC.log_gmc([("Det", self.mat[i], f"= {self.mat[i].det():g}" if self.mat[i].det() != Matrix.ERROR_CODE else Matrix.ERROR_CODE)]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 66, anchor="center")      

            # invert buttons
            tk.Button(self.panel, text="Invert", width=17, height=1, command=lambda i=i:
            (GMC.log_gmc([("", self.mat[i]), ("^(-1) =", self.mat[i].invert())]))).place(    
                x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 66, anchor="center")

            # tranpose buttons
            tk.Button(self.panel, text = "Transpose", width=17, height=1, command=lambda i=i:
            (GMC.log_gmc([("Transpose", self.mat[i]), ("=", self.mat[i].transpose())]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y = c.MATRIX_OP_BASE_Y + 33, anchor="center")
            
            tk.Button(self.panel, text="Visualise", width=17, height=1, command=lambda i=i:
            (self.app.windows[2].visualise_matrix(self.mat[i]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y, anchor="center")
            
            tk.Button(self.panel, text="Rank", width=17, height=1, command=lambda i=i:
            (GMC.log_gmc([("Rank", self.mat[i], f"= {self.mat[i].rank():g}")]))).place(
                x = c.MATRIX_X_BASE - c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y + 99, anchor="center")
            
            tk.Button(self.panel, text="Row Echelon Form", width=17, height=1, command=lambda i=i:
             (GMC.log_gmc([("", self.mat[i]), ("~", Matrix.row_echelon_form(self.mat[i]))]))).place(
                x = c.MATRIX_X_BASE + c.MATRIX_OP_X_SPACING + i * c.MATRIX_X_BASE_DIF, y=c.MATRIX_OP_BASE_Y + 99, anchor="center")