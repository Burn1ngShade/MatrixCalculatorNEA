from __future__ import annotations
from tkinter import messagebox
import inspect
from error_handler import Error_Handler as err

# base class for matrix representation 
# uses [x][y] representation for matrix rather than standard [y][x] for matrix, as it's what im use to
class Matrix:        
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        
        self.set(0)
        
    # --- CONSTRUCTORS ---
        
    @staticmethod
    def from_list_string(str, width, height):
        mat = Matrix(width, height)
        contents = str.split(',')
        for x in range(width):
            for y in range(height):
                mat.content[x][y] = float(contents[x * y + y])     
                
        return mat
        
    @staticmethod
    def copy(mat : Matrix):
        c_mat = Matrix(mat.width, mat.height)
        c_mat.set_from_mat(mat)
        return c_mat
    
    @staticmethod
    def cut(mat : Matrix, x, y): #cuts row and coloum out of matrix and returns smaller matrice 
        new_mat = Matrix.copy(mat)
        new_mat.content = [row for i, row in enumerate(mat.content) if i != x]
        new_mat.content = [ [elem for j, elem in enumerate(row) if j != y] for row in new_mat.content]
        new_mat.set_width(mat.width - 1)
        new_mat.set_height(mat.height - 1)
        
        return new_mat
    
    @staticmethod
    def slice(mat : Matrix, x, y, width, height):
        print(x, y, width, height)
        new_mat = Matrix(width, height)
        for new_y in range(height):
            for new_x in range(width):
                new_mat.content[new_x][new_y] = mat.content[x + new_x][y + new_y]
        return new_mat
    
    @staticmethod 
    def identiy(size):
        size = max(1, min(4, size))
        i_mat = Matrix(size, size)
        for i in range(size):
            i_mat.content[i][i] = 1
        return i_mat
    
    # --- PROPERTYS ---
    
    @property
    def is_square(self): # returns if the matrix is square or not
        return self.width == self.height
    
    @property
    def is_identity(self):
        for y in range(self.height):
            for x in range(self.width):
                if x == y and self.content[x][y] != 1: return False
                if x != y and self.content[x][y] != 0: return False
        return True
    
    # --- FUNCTIONS ---
    
    def swap_row(self, row_a, row_b):
        for x in range(self.width):
            self.content[x][row_a], self.content[x][row_b] = self.content[x][row_b], self.content[x][row_a] 
    
    
        
    def set_width(self, width): # sets the width of the matrix
        self.width = min(max(width, 1), 4)
        self.set(0)
        
    def set_height(self, height): # sets the height of the matrix
        self.height = min(max(height, 1), 4)
        self.set(0)
        
    def set(self, value, override = False): # fill the matrix with given value
        new_content = []
        for x in range(self.width):
            new_content.append([])
            for y in range(self.height):
                if not override and x < len(self.content) and y < len(self.content[0]): new_content[x].append(self.content[x][y])
                else: new_content[x].append(value)
        self.content = new_content
        
    def set_from_values(self, values):
        for x in range(self.width):
            for y in range(self.height):
                self.content[x][y] = values[self.width * y + x]
        
    def set_from_mat(self, mat : Matrix):
        self.set_width(mat.width)
        self.set_height(mat.height)
        
        for x in range(self.width):
            for y in range(self.height):
                self.content[x][y] = mat.content[x][y]
        
    def print(self):  
        print(inspect.currentframe().f_back.f_code.co_name)
        print(self.to_string())
    
    def to_string(self):
        col_max_length = []
        for x in range(self.width):
            col_max_length.append(0)
            for y in range(self.height):
                if self.content[x][y] == 0: self.content[x][y] = 0 # i know this line looks stupid, but it converts all -0.0 from showing as -0 in console or display
                col_max_length[x] = max(col_max_length[x], len(f"{self.content[x][y]:g}"))
        
        s = ""
        for y in range(self.height):
            row = "["
            for x in range(self.width):
                row += f"{self.content[x][y]:g}"
                row += " " * (col_max_length[x] + 1 - len(f"{self.content[x][y]:g}"))
            row = row[:-1] + "]"
            s += f"{row}\n"
        s = s[:-1]
        
        return s
    
    def to_list_string(self):
        s = ""
        for x in range(self.width):
            for y in range(self.height):
                s += f"{self.content[x][y]},"
        return s[:-1]

    # single matrix methods

    def scalar_multiply(self, factor):
        mat_result = Matrix(self.width, self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                mat_result.content[x][y] = self.content[x][y] * factor
        
        mat_result.print()
        return mat_result
    
    def to_pow(self, factor):
        if not self.is_square: 
            return err.raise_error_adv("E110")
    
        if abs(factor) > 10:
            return err.raise_error_adv("E200") 
        
        if factor == 0: return Matrix.identiy(self.width) # A^0 = I (list x^0 = 1)
        
        mat_result = Matrix.copy(self)
        for i in range(int(abs(factor) - 1)):
            mat_result = Matrix.multiply_matrice(mat_result, self)
            
        if factor < 0:
            mat_result_invert = mat_result.invert()    
            if mat_result_invert == False: return False
            mat_result = mat_result_invert
            
        mat_result.print()
        return mat_result
    
    def transpose(self):
        trn_mat = Matrix(self.height, self.width)
        for x in range(self.width):
            for y in range(self.height):
                trn_mat.content[y][x] = self.content[x][y]
                
        return trn_mat
    
    def invert(self):
        if not self.is_square:
            return err.raise_error_adv("E111")
        
        det = self.det()
        if det == 0:
            return err.raise_error_adv("E101")
        
        inv_mat = Matrix.copy(self)
        
        if self.width == 1:
            inv_mat.content[0][0] = 1/det
            return inv_mat
        
        for x in range(inv_mat.width):
            for y in range(inv_mat.height):
                inv_mat.content[x][y] = (-1)**(x + y) * Matrix.cut(self, x, y).det() #get the minor for this part of the matrix
        
        inv_mat = inv_mat.scalar_multiply(1/det)
        inv_mat = inv_mat.transpose()
        
        return inv_mat
            
            
    def det(self): #i think this function counts as recursive?
        if not self.is_square:
            return err.raise_error_adv("E112")
        
        if self.width == 1:
            return self.content[0][0]
        
        if self.width == 2: #2 x 2 matrix
            return (self.content[0][0] * self.content[1][1]) - (self.content[0][1] * self.content[1][0])
        
        if self.width == 3: #3 x 3 matrix
            return (self.content[0][0] * Matrix.cut(self, 0, 0).det() 
            - self.content[1][0] * Matrix.cut(self, 1, 0).det() 
            + self.content[2][0] * Matrix.cut(self, 2, 0).det())
        
        if self.width == 4: #4 x 4 matrix
            return (self.content[0][0] * Matrix.cut(self, 0, 0).det()
            - self.content[1][0] * Matrix.cut(self, 1, 0).det()
            + self.content[2][0] * Matrix.cut(self, 2, 0).det()
            - self.content[3][0] * Matrix.cut(self, 3, 0).det() 
            )
            
    # x-0
    def in_format(self, format):
        #example format for 3x3 1,0,0,0,x,x,0,x,x
        split_format = format.split(',')
        
        variables = {}
        
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                try:
                    if self.content[x][y] != float(split_format[index]): 
                        print(x, y)
                        print(split_format[index], self.content[x][y])
                        self.print()
                        return False
                except ValueError:
                    var = split_format[index][0]
                    
                    if var not in variables:
                        if 'S' in split_format[index][1:]: 
                            if abs(self.content[x][y]) > 1:
                                print("yo") 
                                return False
                        
                        if '-' in split_format[index][1:]: 
                            print("YOOOO")
                            variables[var] = -self.content[x][y]
                        else: 
                            variables[var] = self.content[x][y]
                            print("yo")
                    else:
                        var_value = variables[var]
                        print(var_value)
                        print(variables[var])
                        if '-' in split_format[index][1:]: 
                            print("WE FLIPPING IT")
                            var_value = -var_value
                        if 'S' in split_format[index][1:]: 
                            if abs(self.content[x][y]) > 1:
                                print("yo2") 
                                return False
                        if var_value != self.content[x][y]: 
                            print(var_value)
                            print(self.content[x][y])
                            return False
                    
        return True
                    
    
    # ROW ECHELON FORM SHIT
    
    def find_non_zero_y(self, x, pivot_y):
        print(x, pivot_y)
        for y in range(pivot_y, self.height):
            if self.content[x][y] != 0:
                return y
        return None
    
    def elem_below(self, x, pivot_y):
        pivot_element = self.content[x][pivot_y]
        for y in range(pivot_y + 1, self.height):
            factor = self.content[x][y] / pivot_element
            for i in range(self.width):
                self.content[i][y] -= factor * self.content[i][pivot_y]
            
    def row_echelon_form(self):
        ref_mat = Matrix.copy(self)
        pivot_y = 0
        
        for x in range(ref_mat.width):
            nonzero_y = ref_mat.find_non_zero_y(x, pivot_y)
            if nonzero_y != None:
                ref_mat.swap_row(pivot_y, nonzero_y)
                
                ref_mat.elem_below(x, pivot_y)
                
                pivot_y += 1
        
        return ref_mat
    
    def rank(self): #find the largest matrix with a det of 0
        ref_mat = self.row_echelon_form()
        print(ref_mat)
        for y in range(ref_mat.height):
            if ref_mat.content[ref_mat.width - 1][y] == 0: return y
        return y + 1
        
        
    # two matrix methods
    
    @staticmethod
    def swap_matrice(mat_a: Matrix, mat_b: Matrix): #swaps the content and size of two matrix
        content = mat_b.content
        
        mat_b.set_width(mat_a.width)
        mat_b.set_height(mat_a.height)
        mat_b.content = mat_a.content
        
        mat_a.set_width(len(content))
        mat_a.set_height(len(content[0]))
        mat_a.content = content
        
    @staticmethod
    def multiply_matrice(mat_a: Matrix, mat_b: Matrix): #finds the dot product of 2 matrice
        if mat_a.width != mat_b.height: #requirement for matrix multiplication
            return err.raise_error_adv("E113")
        
        mat_result = Matrix(mat_b.width, mat_a.height)
        
        for y in range(mat_a.height): #loop through each row in mat
            for x in range(mat_b.width): #each row must be compared with every column
                cell_total = 0
                for i in range(mat_a.width): #now multiply elements (could also use height of mat_b)
                    cell_total += mat_a.content[i][y] * mat_b.content[x][i]
                mat_result.content[x][y] = cell_total
                
        return mat_result
    
    @staticmethod
    def add_sub_matrice(mat_a: Matrix, mat_b: Matrix, subtract = False): #add or sub together the scalar values of two matrix
        if mat_a.width != mat_b.width or mat_a.height != mat_b.height:
            return err.raise_error("E114", "Subtract" if subtract else "Add")
        
        mat_result = Matrix(mat_a.width, mat_a.height) #same dimensions
        
        for y in range(mat_a.height):
            for x in range(mat_b.width):
                mat_result.content[x][y] = mat_a.content[x][y] + (-mat_b.content[x][y] if subtract else mat_b.content[x][y]) 
                
        mat_result.print()
        return mat_result
                
        
                    
                    
                
        
        
        
        

            
    
                
        
