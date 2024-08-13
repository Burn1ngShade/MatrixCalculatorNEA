from tkinter import messagebox

class Error_Handler:
    #first number for screen (0 -> login... 9-> debug, next 2 for index)
    error_codes = {
        #login
        "E000" : "Invalid Username", 
        "E001" : "Invalid Password",
        #matrix 
        "E100" : "Invalid Matrice", 
        "E101" : "Invalid Calculation",
        #visualisation
        "E200" : "Dimension Error",
        #sql
        "E300" : "SQL Connection Error",
        #debug
        "E900" : "Not Implemented",
        "E901" : "Work In Progress",
    }
    
    #raises warning message to the user
    @staticmethod
    def raise_error(error_code, message):
        messagebox.showinfo(Error_Handler.error_codes[error_code] + f" [{error_code}]", message)
        return error_code

    @staticmethod
    def is_error(message):
        return message in Error_Handler.error_codes

    @staticmethod
    def raise_promt(question, message):
        return messagebox.askquestion(question, message) == 'yes'