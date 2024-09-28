from tkinter import messagebox
import constants as c

# responsible for handling errors and relaying them to user
class Error_Handler:     
    # --- FUNCTIONS ---
    @staticmethod # raises error of given code to user, filling in any needed parameters
    def raise_error(error_code, parameters = []):
        error_title = c.ERROR_CODES[error_code][0]
        error_message = c.ERROR_CODES[error_code][1]
        
        if isinstance(parameters, str):
            parameters = [parameters]
        for parameter in parameters:
            error_message = error_message.replace("[x]", str(parameter), 1)
        
        messagebox.showinfo(error_title, error_message)
        return False

    @staticmethod # raises yes no promt to the user
    def raise_promt(question, message):
        return messagebox.askquestion(question, message) == 'yes'