from tkinter import messagebox

#first number for screen (0 -> login... 9-> debug, next 2 for index)
error_codes = {
    #login
    "E000" : "Invalid Username", 
    "E001" : "Invalid Password",
    #matrix 
    "E100" : "Invalid Matrice", 
    #visualisation
    "E200" : "Dimension Error",
    #debug
    "E900" : "Not Implemented",
    "E901" : "Work In Progress",
    }

#raises warning message to the user
def raise_error(error_code, message):
    messagebox.showinfo(error_codes[error_code] + f" [{error_code}]", message)
    return error_code

def is_error(message):
    return message in error_codes

def raise_promt(question, message):
    return messagebox.askquestion(question, message) == 'yes'

#validate if input is suitable for matrix and applys update to matrix
def validate_mat_input(value, widget_name, mat):
    widget_index = int(widget_name[15:17])
    print(widget_index)
        
    if len(value) == 0 or value == '-': #case the entry box is empty
        mat.content[widget_index % mat.width][widget_index // mat.width] = 0
        return True
    if value: #general case
        try:
            float(value)
            mat.content[widget_index % mat.width][widget_index // mat.width] = float(value)
            return True
        except ValueError:
            return False
    else:
        return False
    
#general validate function
def validate_input(value):    
    if len(value) == 0 or value == "-":
        return True
    if value:
        try:
            float(value)
            return True
        except ValueError:
            return False

def validate_int_input(value):
    if "." in value: return False
    
    if len(value) == 0 or value == '-':
        return True
    if value:
        try:
            float(value)
            if float(value) % 1 != 0: return False
            return True
        except ValueError:
            return False
