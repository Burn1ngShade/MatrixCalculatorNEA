from tkinter import messagebox
import constants as c

class Error_Handler: # responsible for handling errors and relaying them to user
    error_codes = {
        # login errors
        "E000" : ("Invalid Username", "Usernames Must Be 5-15 Characters."),
        "E001" : ("Invalid Username", f"Username Can Not Be {c.GUEST_USERNAME}."),
        "E002" : ("Invalid Username", "Account With Username [x] Does Not Exist."),
        "E003" : ("Invalid Username", "Username Is Already Taken."),
        "E010" : ("Invalid Password", f"Passwords Must Be 5-15 Characters." ),
        "E011" : ("Invalid Password", "Password Is Incorrect."),
        # matrix
        "E100" : ("Invalid Determinant", "Matrice Raised To A Negative Power Can't Have A Determinant Of 0."), 
        "E101" : ("Invalid Determinant", "Matrice With A Determinant Of 0 Can't Be Inverted."), 
        "E110" : ("Invalid Dimensions", "Only Square Matrice Can Be Raised To A Power."),
        "E111" : ("Invalid Dimensions", "Only Square Matrice Can Be Inverted."),
        "E112" : ("Invalid Dimensions", "Only Square Matrice Have Determinants."),
        "E113" : ("Invalid Dimensions", "Matrix A Must Have The Same Number Of Columns As Matrix B Has Rows."),
        "E114" : ("Invalid Dimensions", "Matrix A And Matrix B Must Be The Same Size To [x]."),
        "E115" : ("Invalid Dimensions", "Matrice Of Dimensions [x]x[x] Can Not Be Visualised. Valid Dimensions: 1x1, 2x2, 3x3, 2x1, 1x2, 3x1, 1x3."),
        # math error
        "E200" : ("Out Of Range", "Powers Must Range Between -10 and 10.")        
    }
    
    # --- FUNCTIONS ---
    
    @staticmethod # raises error of given code to user, filling in any needed parameters
    def raise_error(error_code, parameters = []):
        error_title = Error_Handler.error_codes[error_code][0]
        error_message = Error_Handler.error_codes[error_code][1]
        
        if isinstance(parameters, str):
            parameters = [parameters]
        for parameter in parameters:
            error_message = error_message.replace("[x]", str(parameter), 1)
        
        messagebox.showinfo(error_title, error_message)
        return False

    @staticmethod # raises yes no promt to the user
    def raise_promt(question, message):
        return messagebox.askquestion(question, message) == 'yes'