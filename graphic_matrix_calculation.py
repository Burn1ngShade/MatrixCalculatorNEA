import tkinter as tk
import constants as c
from matrix import Matrix
from database_connection import Database_Connection
import time
from data_handler import Data_Handler

class Graphic_Matrix_Calculation():    
    calculations = []
    current_page = 0
    
    database_entrys_to_remove = []
    sort_method = 0
    
    @staticmethod
    def init(window):
        Graphic_Matrix_Calculation.window = window
        
    def __init__(self, matrices : list, creation_date = -1, matrix_calculation_id = -1):
        self.panel = Graphic_Matrix_Calculation.window.panel
        self.matrices = matrices
        self.graphic = False
        
        # database info
        self.creation_date = time.time() if creation_date < 0 else creation_date
        self.matrix_calculation_id = matrix_calculation_id

        Graphic_Matrix_Calculation.calculations.append(self)

    def create(self, y = c.MATRIX_CALC_BASE_Y): # creates graphic for the calculation
        self.graphic = True
        
        self.frame = tk.Frame(self.panel, bg="gainsboro", width = 780, height = 81)
        self.frame.option_add( "*font", "Consolas 8" )
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
        (self.destroy(), Graphic_Matrix_Calculation.database_entrys_to_remove.append(self.matrix_calculation_id))).place(
        x=758, y=3)
        
        if len(self.matrices) <= 1: return # not a matrix operation so no resultant matrix
        
        if f"{self.matrices[-1][1].height}x{self.matrices[-1][1].width}" in c.VALID_VISUAL_MATRIX_DIMENSIONS:
            tk.Button(self.frame, text="Visualise", width= 14, height=1, command=lambda:
                (self.window.app.windows[2].visualise_matrix(self.matrices[-1][1]))).place(x = 662, y=3)
        tk.Button(self.frame, text="Insert In A", width=17, height=1, command=lambda:
        (Graphic_Matrix_Calculation.window.mat[0].set_from_mat(self.matrices[-1][1]), Graphic_Matrix_Calculation.window.mat[0].draw())).place(x = 662, y=29)
        tk.Button(self.frame, text="Insert In B", width=17, height=1, command=lambda:
        (Graphic_Matrix_Calculation.window.mat[1].set_from_mat(self.matrices[-1][1]), Graphic_Matrix_Calculation.window.mat[1].draw())).place(x = 662, y=55)
        
    def hide(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame.destroy()
        self.graphic = False

        Graphic_Matrix_Calculation.update_gmc_list()

    def destroy(self): # destroys graphic for the calculation
        Graphic_Matrix_Calculation.calculations.remove(self)        
        if self.graphic: self.hide()

    def move(self, y): # move graphic
        self.frame.place(x = 10, y = y)

    # static methods

    @staticmethod
    def log_gmc(matrice, creation_date=-1, matrix_calculation_id=-1):        
        for i in range(len(matrice)): #check for error in calculation 
                if isinstance(matrice[i][1], bool) and matrice[i][1] == False: return 
                if len(matrice[i]) > 2:
                    print(matrice[i][2])
                    if (isinstance(matrice[i][2], bool) and matrice[i][2] == False): return
                
        for i in range(len(matrice)):
            matrice[i] = (matrice[i][0], Matrix.copy(matrice[i][1])) if len(matrice[i]) <= 2 else (matrice[i][0], Matrix.copy(matrice[i][1]), matrice[i][2]) 

        gmc = Graphic_Matrix_Calculation(matrice, creation_date, matrix_calculation_id)
        if Graphic_Matrix_Calculation.sort_method != 0: Graphic_Matrix_Calculation.sort()
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
                
        Graphic_Matrix_Calculation.window.prev_trans_text.config(text = 
        f"Previous Matrix Calculations --- Page [{Graphic_Matrix_Calculation.current_page + 1} / {Graphic_Matrix_Calculation.gmc_page_count()}]")

    @staticmethod
    def update_gmc_page(page):
        Graphic_Matrix_Calculation.current_page = max(0, min(page, Graphic_Matrix_Calculation.gmc_page_count() - 1))
        Graphic_Matrix_Calculation.update_gmc_list()

    @staticmethod
    def gmc_page_count():
        return (max(len(Graphic_Matrix_Calculation.calculations) - 1, 0) // 5) + 1
    
    @staticmethod
    def save_matrix_calculations(account_name):
        db_con = Database_Connection()
        user_id = db_con.get_record("Users", "Username", account_name)[0]
        
        for id in Graphic_Matrix_Calculation.database_entrys_to_remove: #delete entrys weve been told to delete
            if id == -1: continue
            db_con.delete_record("MatrixCalculations", "MatrixCalculationID", id)
            db_con.delete_record("MatrixCalculationElements", "MatrixCalculationID", id)
            
        Graphic_Matrix_Calculation.database_entrys_to_remove = []
        
        for calc in Graphic_Matrix_Calculation.calculations:
            if calc.matrix_calculation_id == -1: #this is a new calculation
                db_con.insert_record("MatrixCalculations", c.MATRIX_CALCULATION_DB_COLUMNS, (user_id, calc.creation_date))
                id = db_con.get_record("MatrixCalculations", "CreationDate", calc.creation_date)[0]
                for m in calc.matrices:
                    db_con.insert_record("MatrixCalculationElements", c.MATRIX_CALCULATION_ELEMENT_DB_COLUMNS, (id, m[0], "" if len(m) < 3 else m[2], m[1].width, m[1].height, m[1].to_list_string()))
                
        # i belive i dont have to touch records already in the database cause duh
    
        db_con.close(True)
            
    @staticmethod 
    def load_matrix_calculations(account_name):
        db_con = Database_Connection()
        user_id = db_con.get_record("Users", "Username", account_name)[0]
        records = db_con.get_record("MatrixCalculations", "UserID", user_id, True)
        
        for record in records:
            matrice_records = db_con.get_record("MatrixCalculationElements", "MatrixCalculationID", record[0], True)
            
            matrice = []
            for r in matrice_records:
                m = Matrix.from_list_string(r[6], r[4], r[5])
                if len(r[3]) > 0: matrice.append((r[2], m, r[3]))
                else: matrice.append((r[2], m))
            
            Graphic_Matrix_Calculation.log_gmc(matrice, float(record[2]), float(record[0]))
            
        db_con.close()
   
    @staticmethod
    def clear_matrix_calculations():
        while len(Graphic_Matrix_Calculation.calculations) > 0:
            Graphic_Matrix_Calculation.calculations[0].destroy()
            
    @staticmethod
    def on_sort_method_select(event, combobox):
        Graphic_Matrix_Calculation.window.panel.focus()
        combobox.selection_clear()
        
        method = c.MATRIX_CALC_SORT_OPTIONS.index(combobox.get())
        
        if method == Graphic_Matrix_Calculation.sort_method: return
        Graphic_Matrix_Calculation.sort_method = method
        Graphic_Matrix_Calculation.sort()
        
    @staticmethod
    def sort():       
        sort_type = Graphic_Matrix_Calculation.sort_method // 2
        sort_reverse = Graphic_Matrix_Calculation.sort_method % 2
        
        if sort_type == 0:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.creation_date for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        elif sort_type == 1:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.matrices[0][1].width * value.matrices[0][1].height for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        elif sort_type == 2:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.matrices[-1][1].rank() for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        
        if sort_reverse == 1: Graphic_Matrix_Calculation.calculations.reverse()

        Graphic_Matrix_Calculation.update_gmc_list()
        

        
        
        
        
