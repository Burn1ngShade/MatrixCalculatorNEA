from error_handler import Error_Handler as err

class Data_Handler:
    # --- INPUT VALIDATION ---
    
    @staticmethod
    def validate_matrix_input(value, widget_name, mat): # validates that a matrix input is valid and updates the given cell 
        widget_index = int(widget_name[15:17]) # get the widget index from name
        
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
    
    @staticmethod
    def validate_float_input(value): # validate given input is a float    
        if len(value) == 0 or value == "-":
            return True
        if value:
            try:
                float(value)
                return True
            except ValueError:
                return False

    @staticmethod
    def validate_int_input(value): # validate given input is a number
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
           
    @staticmethod 
    def validate_string_length(message, error_code, min = 5, max = 15): # validate given input is between a min and max length
        if len(message) < min or len(message) > max: return err.raise_error(error_code)
        return True
    
    # --- SORTING ---
    
    @staticmethod
    def sort(value_array, sort_array): # carrys out merge sort on given values, using associated sort value 
        array = list(zip(value_array, sort_array))
        Data_Handler._merge_sort(array, 0, len(array) - 1)
        return [value[1] for value in array]
    
    @staticmethod
    def _merge_sort(array, left, right): # split array into two segements
        if left < right: # if array can still be divided in length
            mid = left+(right-left)//2
            # sort both halfs of array
            Data_Handler._merge_sort(array, left, mid)
            Data_Handler._merge_sort(array, mid+1, right)
            Data_Handler._merge(array, left, mid, right)
        
    @staticmethod
    def _merge(array, left, mid, right):
        left_array_len = mid - left + 1
        left_array = [0] * (left_array_len)
        for i in range(0, left_array_len):
            left_array[i] = array[left + i]
 
        right_array_len = right - mid
        right_array = [0] * (right_array_len)
        for j in range(0, right_array_len):
            right_array[j] = array[mid + 1 + j]
 
        i, j, k = 0, 0, left # index of left_array, right_array and merged array 
 
        while i < left_array_len and j < right_array_len:
            if left_array[i][0] <= right_array[j][0]:
                array[k] = left_array[i]
                i += 1
            else:
                array[k] = right_array[j]
                j += 1
            k += 1
 
        while i < left_array_len:
            array[k] = left_array[i]
            i += 1
            k += 1
 
        while j < right_array_len:
            array[k] = right_array[j]
            j += 1
            k += 1
