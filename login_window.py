import tkinter as tk
import constants as c
from database_connection import Database_Connection
from error_handler import Error_Handler as err
from data_handler import Data_Handler as dh
from window import Window

class Login_Window(Window): # window for login and creating accounts
    def __init__(self, app):
        super().__init__(app)
        
    # --- SETUP ---
           
    def setup_window(self): # draw all elements in window    
        self.setup_title()
        self.setup_login_buttons()
        
    def setup_title(self): # setup title background and icon
        tk.Frame(self.panel, bg="gainsboro", height=230).pack(side=tk.TOP, fill=tk.X)
        self.title_image = tk.PhotoImage(file="Assets/Title.png") # must be saved to stop garbage collection removing 
        tk.Label(self.panel, image=self.title_image, bg="gainsboro").place(x = 400, y = 105, anchor="center")
    
    def setup_login_buttons(self): # setup login backgrounds and buttons
        # frames
        center_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=140)
        center_panel.place(x=400, y=335, anchor="center")
        left_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=100)
        left_panel.place(x=145, y=385, anchor="center")
        right_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=100)
        right_panel.place(x=655, y=385, anchor="center")
        center_bot_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=50)
        center_bot_panel.place(x=400, y=465, anchor="center")
        
        # username and password entry
        tk.Label(center_panel, text="Username", bg = "gainsboro").place(x = 110, y = 15, anchor="center")
        self.login_username = tk.Entry(center_panel, width=18)
        self.login_username.place(x = 110, y = 40, anchor="center")
        tk.Label(center_panel, text="Password", bg = "gainsboro").place(x = 110, y = 80, anchor="center")
        self.login_pswd = tk.Entry(center_panel, width=18)
        self.login_pswd.place(x = 110, y = 105, anchor="center")
        
        # buttons
        tk.Button(left_panel, width=20, height=1, text="Create Account", command=lambda:
            self.try_create_account(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 25, anchor="center")
        tk.Button(left_panel, width=20, height=1, text="Delete Account", command=lambda:
            self.try_account_delete(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 75, anchor="center")
        tk.Button(right_panel, width=20, height=1, text="Login To Account", command=lambda:
            self.try_account_login(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 25, anchor="center")
        tk.Button(right_panel, width=20, height=1, text=f"Continue As {c.GUEST_USERNAME}", command=lambda:
            self.app.open_window(1)).place(x = 110, y = 75, anchor="center")
        tk.Button(center_bot_panel, width=20, height=1, text="Exit Application",
            command=self.application_quit).place(x=110, y=25, anchor="center")
            
    # --- LOGIN FUNCTIONS ---
        
    def try_create_account(self, username, password): # create new account        
        if not dh.validate_string_length(username, "E000") or not dh.validate_string_length(password, "E010"): return False
        if username == c.GUEST_USERNAME: return err.raise_error_adv("E001")
        
        db_con = Database_Connection()
        if db_con.get_record("Users", "Username", username) != None: return err.raise_error_adv("E003")
        db_con.insert_record("Users", c.USER_DB_COLUMNS, (username, password))
        db_con.close(True)
        
        self.app.load_account(username)
        self.app.open_window(1)
        
    def try_account_login(self, username, password): # login to existing account
        db_con = Database_Connection()
        record = db_con.get_record("Users", "Username", username)
        db_con.close()
        
        if record == None: return err.raise_error_adv("E002", username)
        if record[2] != password: return err.raise_error_adv("E011")
        
        self.app.load_account(username)
        self.app.open_window(1)
        
    def try_account_delete(self, username, password): # delete an existing account
        db_con = Database_Connection()
        record = db_con.get_record("Users", "Username", username)
        
        if record == None: return err.raise_error_adv("E002", username)
        if record[2] != password: return err.raise_error_adv("E011")
        
        if err.raise_promt(f"Delete Account [{username}]", f"Are You Sure You Want To Delete This Account? This Action Can Not Be Undone."):
            matrix_calc = db_con.get_record("MatrixCalculations", "UserID", record[0], True)
            for mat in matrix_calc:
                db_con.delete_record("MatrixCalculations", "MatrixCalculationID", mat[0])
                db_con.delete_record("MatrixCalculationElements", "MatrixCalculationID", mat[0])
            db_con.delete_record("Users", "Username", username)
        db_con.close(True)

    def application_quit(self): # raise promt to close application to user
        if err.raise_promt("Quit Application", "Are You Sure You Want To Close Matrix Caculator?"):
            self.app.root.destroy()
        
        
