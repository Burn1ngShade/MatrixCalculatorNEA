import tkinter as tk
import entry_validation as val
import database_handler

class Login_Window:
    def __init__(self, app):
        self.app = app
        
        self.panel = tk.Frame(app.root, bg="snow3")
        self.panel.option_add( "*font", "Consolas 12" )
        self.panel.place(relx=0, rely=0, relwidth=1, relheight=1)

        #frames
        tk.Frame(self.panel, bg="gainsboro", height=230).pack(side=tk.TOP, fill=tk.X)  # Pack the frame at the top and fill horizontally
        
        user_pswd_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=140)
        user_pswd_panel.place(x=400, y=335, anchor="center")
        right_button_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=100)
        right_button_panel.place(x=655, y=385, anchor="center")
        center_button_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=50)
        center_button_panel.place(x=400, y=465, anchor="center")
        left_button_panel = tk.Frame(self.panel, bg="gainsboro", width=220, height=100)
        left_button_panel.place(x=145, y=385, anchor="center")
        
        #title
        self.title_image = tk.PhotoImage(file="Assets/Title.png")
        tk.Label(self.panel, image=self.title_image, bg="gainsboro").place(x = 400, y = 105, anchor="center")
        
        # username
        tk.Label(user_pswd_panel, text="Username", bg = "gainsboro").place(x = 110, y = 15, anchor="center")
        self.login_username = tk.Entry(user_pswd_panel, width=18)
        self.login_username.place(x = 110, y = 40, anchor="center")
        
        # password
        tk.Label(user_pswd_panel, text="Password", bg = "gainsboro").place(x = 110, y = 80, anchor="center")
        self.login_pswd = tk.Entry(user_pswd_panel, width=18)
        self.login_pswd.place(x = 110, y = 105, anchor="center")
        
        # buttons
        tk.Button(left_button_panel, width=20, height=1, text="Create Account", command=lambda:
            self.account_create(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 25, anchor="center")
        tk.Button(left_button_panel, width=20, height=1, text="Delete Account", command=lambda:
            self.account_delete(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 75, anchor="center")
        
        tk.Button(right_button_panel, width=20, height=1, text="Login To Account", command=lambda:
            self.account_login(self.login_username.get(), self.login_pswd.get())).place(x = 110, y = 25, anchor="center")
        tk.Button(right_button_panel, width=20, height=1, text="Continue As Guest", command=lambda:
            self.app.open_window(1)).place(x = 110, y = 75, anchor="center")
        
        tk.Button(center_button_panel, width=20, height=1, text="Exit Application",
            command=self.application_quit).place(x=110, y=25, anchor="center")
        
        
    def validate_username(self, username):
        if len(username) < 5 or len(username) > 15: return val.raise_error("E000", "Usernames Must Be 5-15 Characters.")
        return True
    
    def validate_password(self, password):
        if len(password) < 5 or len(password) > 15: return val.raise_error("E001", "Passwords Must Be 5-15 Characters.")
        return True    
        
    def account_create(self, username, password):
        if val.is_error(self.validate_username(username)) or val.is_error(self.validate_password(password)): return False
        if username == "Guest": return val.raise_error("E000", "Username Can Not Be Guest.")
        if database_handler.get_record("Users", "Username", username) != None: return val.raise_error("E000", "Username Is Already Taken.")

        database_handler.insert_record("Users", "Username, Password", (username, password))
        self.app.load_account(username)
        self.app.open_window(1)
        
    def account_login(self, username, password):
        record = database_handler.get_record("Users", "Username", username)
        if record == None: return val.raise_error("E000", f"Account With Username [{username}] Does Not Exist.")
        if record[2] != password: return val.raise_error("E001", f"Password Is Incorrect.")
        self.app.load_account(username)
        self.app.open_window(1)
        
    def account_delete(self, username, password):
        record = database_handler.get_record("Users", "Username", username)
        if record == None: return val.raise_error("E000", f"Account With Username [{username}] Does Not Exist.")
        if record[2] != password: return val.raise_error("E001", f"Password Is Incorrect.")
        if val.raise_promt(f"Delete Account [{username}]", f"Are You Sure You Want To Delete This Account? This Action Can Not Be Undone."):
            database_handler.delete_record("Users", "Username", username)

    def application_quit(self):
        if val.raise_promt("Quit Application", "Are You Sure You Want To Close Matrix Caculator?"):
            self.app.root.destroy()
        
        
