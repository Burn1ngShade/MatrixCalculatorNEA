import tkinter as tk
import constants as c
from matrix import Matrix

class Graphic_Matrix_Calculation():
    target_window = None
    
    calculations = []
    current_page = 0
    
    def __init__(self, matrices : list):
        self.panel = Graphic_Matrix_Calculation.target_window.panel
        self.matrices = matrices

        self.graphic = False

        Graphic_Matrix_Calculation.calculations.append(self)

    def create(self, y = c.MATRIX_CALC_BASE_Y): # creates graphic for the calculation
        self.graphic = True
        
        self.frame = tk.Frame(self.panel, bg="gainsboro", width = 780, height = 81)
        self.frame.place(x = 10, y = y, anchor="w")
        
        x_offset = 10
        for mat in self.matrices:
            if len(mat[0]) > 0: 
                tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=mat[0]).place(x=x_offset, y=42, anchor="w")
                x_offset += len(mat[0]) * 9 + 5
                
            mat_text = mat[1].to_string()
            tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=f"{mat_text}").place(x=x_offset, y=42, anchor="w")
            x_offset += (len(mat_text[:mat_text.find('\n')]) * 9) if '\n' in mat_text else len(mat_text) * 9
            x_offset += 5
            
            if len(mat) > 2 and len(mat[2]) > 0: 
                tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=mat[2]).place(x=x_offset, y=42, anchor="w")
                x_offset += len(mat[0]) * 9 + 5
                
        #buttons

        tk.Button(self.frame, text="X", width=1, height=1, command=lambda:
        (self.destroy())).place(
        x=758, y=3)
        
        if len(self.matrices) <= 1: return # not a matrix operation so no resultant matrix
        
        tk.Button(self.frame, text="Visualise", width= 14, height=1, command=lambda:
        (self.target_window.app.windows[2].visualise_matrix(self.matrices[-1][1]))).place(x = 662, y=3)
        tk.Button(self.frame, text="Insert In A", width=17, height=1, command=lambda:
        (Graphic_Matrix_Calculation.target_window.mat_a.set_from_mat(self.matrices[-1][1]), Graphic_Matrix_Calculation.target_window.mat_a.draw())).place(x = 662, y=29)
        tk.Button(self.frame, text="Insert In B", width=17, height=1, command=lambda:
        (Graphic_Matrix_Calculation.target_window.mat_b.set_from_mat(self.matrices[-1][1]), Graphic_Matrix_Calculation.target_window.mat_b.draw())).place(x = 662, y=55)
        
    def hide(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame.destroy()
        self.graphic = False

        Graphic_Matrix_Calculation.update_gmc_list()

    def destroy(self): # destroys graphic for the calculation
        Graphic_Matrix_Calculation.calculations.remove(self)
        self.hide()

    def move(self, y): # move graphic
        self.frame.place(x = 10, y = y)

    # static methods

    @staticmethod
    def log_gmc(matrice):
        for i in range(len(matrice)): #check for error in calculation 
                if matrice[i][1] == Matrix.ERROR_CODE: return 
                if len(matrice[i]) > 2 and Matrix.ERROR_CODE in matrice[i][2]: return

        gmc = Graphic_Matrix_Calculation(matrice)
        gmc.update_gmc_list()

    @staticmethod
    def update_gmc_list(): 
        Graphic_Matrix_Calculation.current_page = min(Graphic_Matrix_Calculation.gmc_page_count() - 1, Graphic_Matrix_Calculation.current_page) #kicks user down a page if deleted all records
        show_start_index = (Graphic_Matrix_Calculation.current_page) * 5
        
        rev_gmc = Graphic_Matrix_Calculation.calculations[::-1]   
        for i in range(len(rev_gmc)):
            if i >= show_start_index and i <= show_start_index + 4:
                if not (rev_gmc[i].graphic): rev_gmc[i].create()
                rev_gmc[i].move(c.MATRIX_CALC_BASE_Y + (i - show_start_index) * c.MATRIX_CALC_INCR_Y)
            else:
                if (rev_gmc[i].graphic): rev_gmc[i].hide()
                
        Graphic_Matrix_Calculation.target_window.prev_trans_text.config(text = 
        f"Previous Matrix Calculations --- Page [{Graphic_Matrix_Calculation.current_page + 1} / {Graphic_Matrix_Calculation.gmc_page_count()}]")

    @staticmethod
    def update_gmc_page(page):
        Graphic_Matrix_Calculation.current_page = max(0, min(page, Graphic_Matrix_Calculation.gmc_page_count() - 1))
        Graphic_Matrix_Calculation.update_gmc_list()

    @staticmethod
    def gmc_page_count():
        return (max(len(Graphic_Matrix_Calculation.calculations) - 1, 0) // 5) + 1
        
        
        