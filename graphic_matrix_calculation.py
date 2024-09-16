import tkinter as tk
import constants as c
from matrix import Matrix
from database_connection import Database_Connection
import time
from data_handler import Data_Handler

# class responsible for saving and displaying a matrix calculation
class Graphic_Matrix_Calculation():    
    deleted_calculations = [] # calculations entrys that have been deleted and need to be removed from the database
    calculations = [] # list of all currently loaded calculations
    current_page = 0 # current page of calculations loaded
    sort_method = 0 # current sort method being used to sort calculations (e.g creation time (ascending))
    
    # --- setup ---
    
    @staticmethod
    def set_target_window(window): # set the window to draw calculations to
        Graphic_Matrix_Calculation.window = window
        
    def __init__(self, calculation_info : list, creation_date = -1, matrix_calculation_id = -1):
        # calculation info
        self.panel = Graphic_Matrix_Calculation.window.panel
        self.calculation_info = calculation_info
        self.currently_rendered = False
        
        # database info
        self.creation_date = round(time.time(), 3) if creation_date < 0 else creation_date 
        self.matrix_calculation_id = matrix_calculation_id # id in the database

        Graphic_Matrix_Calculation.calculations.append(self)

    # --- GRAPHICS ---

    def draw_to_panel(self, y = c.MATRIX_CALC_BASE_Y): # creates graphic for the calculation
        self.currently_rendered = True
        
        self.frame = tk.Frame(self.panel, bg="gainsboro", width = 780, height = 81)
        self.frame.option_add( "*font", "Consolas 8" )
        self.frame.place(x = 10, y = y, anchor="w")
        
        # calculation visualse representation
        x_offset = 10
        for mat in self.calculation_info:
            if len(mat[0]) > 0: # if we have prefix text e.g. det [MATRIX]
                tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=mat[0]).place(x=x_offset, y=42, anchor="w")
                x_offset += len(mat[0]) * 9 + 5
                
            # visualise actual matrix
            mat_text = mat[1].to_string()
            tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=f"{mat_text}").place(x=x_offset, y=42, anchor="w")
            x_offset += (len(mat_text[:mat_text.find('\n')]) * 9) if '\n' in mat_text else len(mat_text) * 9
            x_offset += 5
            
            if len(mat) > 2 and len(mat[2]) > 0: # if we have suffix text e.g. [MATRIX] = 2
                tk.Label(self.frame, bg="gainsboro", font=("Consolas", 12), text=mat[2]).place(x=x_offset, y=42, anchor="w")
                x_offset += len(mat[0]) * 9 + 5
                
        #buttons
        tk.Button(self.frame, text="X", width=1, height=1, command=lambda: # delete from history button
        (self.hard_destroy(), Graphic_Matrix_Calculation.deleted_calculations.append(self.matrix_calculation_id))).place(
        x=758, y=3)
        
        if len(self.calculation_info) <= 1: return # calculation does not result in a matrix result so we can return
        
        if self.calculation_info[-1][1].dimensions in c.VALID_VISUAL_MATRIX_DIMENSIONS: # if can be visualised
            tk.Button(self.frame, text="Visualise", width= 14, height=1, command=lambda:
                (self.window.app.windows[2].visualise_matrix_transformation(self.calculation_info[-1][1]))).place(x = 662, y=3)
            
        tk.Button(self.frame, text="Insert In A", width=17, height=1, command=lambda:
            (Graphic_Matrix_Calculation.window.mat[0].set_from_mat(self.calculation_info[-1][1]), Graphic_Matrix_Calculation.window.mat[0].draw_to_panel())).place(x = 662, y=29)
        tk.Button(self.frame, text="Insert In B", width=17, height=1, command=lambda:
            (Graphic_Matrix_Calculation.window.mat[1].set_from_mat(self.calculation_info[-1][1]), Graphic_Matrix_Calculation.window.mat[1].draw_to_panel())).place(x = 662, y=55)
        
    def soft_destroy(self): # destroys the graphics from the panel while keeping the data within the calculations array
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame.destroy()
        self.currently_rendered = False

        Graphic_Matrix_Calculation.update_calculation_list()

    def hard_destroy(self): # destroys graphic from the panel and from calculations list all together
        Graphic_Matrix_Calculation.calculations.remove(self)        
        if self.currently_rendered: self.soft_destroy()

    def set_panel_position(self, y): # move graphic to given panel position
        self.frame.place(x = 10, y = y)

    # --- CALCULATION LIST AND DATABASE HANDLING

    @staticmethod
    def log_calculation(matrice, creation_date=-1, matrix_calculation_id=-1):  
        for i in range(len(matrice)): #check for error code in calculation (results can only be string or matrix so if its a bool its an error)
                if isinstance(matrice[i][1], bool): return # standard if == False cant be used as 0 evaluates to false
                if len(matrice[i]) > 2:
                    if (isinstance(matrice[i][2], bool)): return
                
        for i in range(len(matrice)): # create a deepy copy of the matrix
            matrice[i] = (matrice[i][0], Matrix.copy(matrice[i][1])) if len(matrice[i]) <= 2 else (matrice[i][0], Matrix.copy(matrice[i][1]), matrice[i][2]) 

        gmc = Graphic_Matrix_Calculation(matrice, creation_date, matrix_calculation_id)
        if Graphic_Matrix_Calculation.sort_method != 0: Graphic_Matrix_Calculation.sort() # if we arent using time created descending we have to resort the list
        gmc.update_calculation_list()

    @staticmethod
    def update_calculation_list(): # updates the list graphically
        Graphic_Matrix_Calculation.current_page = min(Graphic_Matrix_Calculation.get_calculation_page_count() - 1, Graphic_Matrix_Calculation.current_page) #kicks user down a page if deleted all records
        show_start_index = (Graphic_Matrix_Calculation.current_page) * 5 #index of first calculation to show
        
        r_calculations = Graphic_Matrix_Calculation.calculations[::-1]
        for i in range(len(r_calculations)):
            if i >= show_start_index and i <= show_start_index + 4:
                if not (r_calculations[i].currently_rendered): r_calculations[i].draw_to_panel()
                r_calculations[i].set_panel_position(c.MATRIX_CALC_BASE_Y + (i - show_start_index) * c.MATRIX_CALC_INCR_Y)
            else:
                if (r_calculations[i].currently_rendered): r_calculations[i].soft_destroy() # hide calculations that have gone out of scope
                
        Graphic_Matrix_Calculation.window.prev_trans_text.config(text = 
        f"Previous Matrix Calculations --- Page [{Graphic_Matrix_Calculation.current_page + 1} / {Graphic_Matrix_Calculation.get_calculation_page_count()}]")

    @staticmethod
    def update_loaded_calculation_page(page): # update the currently displayed page
        Graphic_Matrix_Calculation.current_page = max(0, min(page, Graphic_Matrix_Calculation.get_calculation_page_count() - 1))
        Graphic_Matrix_Calculation.update_calculation_list()

    @staticmethod
    def get_calculation_page_count(): # returns the number of pages needed for all calculations
        return (max(len(Graphic_Matrix_Calculation.calculations) - 1, 0) // 5) + 1
    
    @staticmethod
    def clear_calculation_list(): # clear the list of all calculations
        while len(Graphic_Matrix_Calculation.calculations) > 0:
            Graphic_Matrix_Calculation.calculations[0].hard_destroy()
    
    # --- LIST DATABASE INTERACTION ---
    
    @staticmethod
    def save_matrix_calculations(account_name): # saves current calculations to database
        db_con = Database_Connection()
        user_id = db_con.get_record("Users", "Username", account_name)[0]
        
        for id in Graphic_Matrix_Calculation.deleted_calculations: #delete entrys weve been told to delete
            if id == -1: continue
            db_con.delete_record("MatrixCalculations", "MatrixCalculationID", id)
            db_con.delete_record("MatrixCalculationElements", "MatrixCalculationID", id)

        Graphic_Matrix_Calculation.deleted_calculations = []
        
        for calc in Graphic_Matrix_Calculation.calculations:
            if calc.matrix_calculation_id == -1: #this is a new calculation
                print(calc.creation_date)
                db_con.insert_record("MatrixCalculations", c.MATRIX_CALCULATION_DB_COLUMNS, (user_id, calc.creation_date))
                print(db_con.get_record("MatrixCalculations", "UserID", 36, True))
                id = db_con.get_record("MatrixCalculations", "CreationDate", calc.creation_date)[0]
                for m in calc.calculation_info: # insert information for each individual element in the matrix
                    db_con.insert_record("MatrixCalculationElements", c.MATRIX_CALCULATION_ELEMENT_DB_COLUMNS, (id, m[0], "" if len(m) < 3 else m[2], m[1].width, m[1].height, m[1].to_database_format()))
    
        db_con.close(True)
            
    @staticmethod 
    def load_account_calculations(account_name): # loads give users database info to calculations
        db_con = Database_Connection()
        user_id = db_con.get_record("Users", "Username", account_name)[0]
        records = db_con.get_record("MatrixCalculations", "UserID", user_id, True)
        
        for record in records:
            matrice_records = db_con.get_record("MatrixCalculationElements", "MatrixCalculationID", record[0], True)
            
            matrice = []
            for r in matrice_records:
                m = Matrix.from_database_format(r[6], r[4], r[5])
                if len(r[3]) > 0: matrice.append((r[2], m, r[3]))
                else: matrice.append((r[2], m))
            
            Graphic_Matrix_Calculation.log_calculation(matrice, float(record[2]), float(record[0]))
            
        db_con.close()
        
    # --- SORT LIST ---
            
    @staticmethod
    def on_sort_method_select(event, combobox): # when the sort method is updated
        Graphic_Matrix_Calculation.window.panel.focus()
        combobox.selection_clear()
        
        method = c.MATRIX_CALC_SORT_OPTIONS.index(combobox.get())
        
        if method == Graphic_Matrix_Calculation.sort_method: return # user reselected the same sort method
        Graphic_Matrix_Calculation.sort_method = method
        Graphic_Matrix_Calculation.sort()
        
    @staticmethod
    def sort():       
        sort_type = Graphic_Matrix_Calculation.sort_method // 2 # type of sort
        sort_reverse = Graphic_Matrix_Calculation.sort_method % 2 # should we go in ascending rather than descending order
        
        if sort_type == 0:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.creation_date for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        elif sort_type == 1:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.calculation_info[0][1].width * value.calculation_info[0][1].height for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        elif sort_type == 2:
            Graphic_Matrix_Calculation.calculations = Data_Handler.sort([value.calculation_info[-1][1].rank() for value in Graphic_Matrix_Calculation.calculations], Graphic_Matrix_Calculation.calculations)
        
        if sort_reverse == 1: Graphic_Matrix_Calculation.calculations.reverse()

        Graphic_Matrix_Calculation.update_calculation_list()
        

        
        
        
        
