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
