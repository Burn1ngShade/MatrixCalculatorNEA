from __future__ import annotations # for type implication for Matrix in Matrix class
from datetime import datetime
import inspect
from error_handler import Error_Handler as err

# base class for matrix representation 
# uses [x][y] representation for matrix rather than standard [y][x] for matrix, as it's what im use to
class Matrix:        
    def __init__(self, width, height):
        self.content = []
        self.set_dimensions(width, height)
        
    # --- CONSTRUCTORS ---
        
    @staticmethod
    def from_database_format(database_string, width, height): # convert database information to a matrix
        mat = Matrix(width, height)
        contents = database_string.split(',')
        for x in range(width):
            for y in range(height):
                mat.content[x][y] = float(contents[x * y + y])     
        return mat
        
    @staticmethod
    def copy(base_mat : Matrix):
        mat = Matrix(base_mat.width, base_mat.height)
        for x in range(mat.width):
            for y in range(mat.height):
                mat.content[x][y] = base_mat.content[x][y]
        return mat
    
    @staticmethod
    def cut(base_mat : Matrix, x, y): # creates a matrix via cutting a given row and column out of a matrix  
        mat = Matrix.copy(base_mat)
        mat.content = [row for i, row in enumerate(base_mat.content) if i != x]
        mat.content = [[elem for j, elem in enumerate(row) if j != y] for row in mat.content]
        mat.set_dimensions(base_mat.width - 1, base_mat.height - 1)
        return mat
    
    @staticmethod 
    def identiy(size):
        size = max(1, min(4, size))
        mat = Matrix(size, size)
        for i in range(size):
            mat.content[i][i] = 1
        return mat
    
    # --- PROPERTYS ---
    
    @property
    def is_square(self): # returns if the matrix is square or not
        return self.width == self.height
    
    @property
    def is_identity(self): # returns if matrix is identity matrix
        for y in range(self.height):
            for x in range(self.width):
                if x == y and self.content[x][y] != 1: return False
                if x != y and self.content[x][y] != 0: return False
        return True
    
    @property
    def dimensions(self):
        return f"{self.height}x{self.width}"
    
    # --- MODIFY FUNCTIONS ---
    
    def set_dimensions(self, width, height): # set dimensions of matrix
        self.width = min(max(width, 1), 4)
        self.height = min(max(height, 1), 4)
        self.refresh()
    
    def swap_rows(self, row_a, row_b): # swap two rows of the matrix
        for x in range(self.width):
            self.content[x][row_a], self.content[x][row_b] = self.content[x][row_b], self.content[x][row_a] 
            
    def swap_columns(self, column_a, column_b): # swap two columns of the matrix
        for y in range(self.height):
            self.content[column_a][y], self.content[column_b][y] = self.content[column_b][y], self.content[column_a][y] 
    
    def refresh(self, clear_matrix = False): # refreshes the content of the matrix with current width and height values
        new_content = []
        for x in range(self.width):
            new_content.append([])
            for y in range(self.height):
                if not clear_matrix and x < len(self.content) and y < len(self.content[0]): new_content[x].append(self.content[x][y])
                else: new_content[x].append(0)
        self.content = new_content
        
    def set_from_list(self, list): # set matrix values from a 1d list of values
        for x in range(self.width):
            for y in range(self.height):
                self.content[x][y] = list[self.width * y + x]
                
    # --- FORMAT FUNCTIONS ---
        
    def print(self): # print out matrix info dump to console for debug purposes
        frame_info = inspect.currentframe().f_back
        
        print("--- Matrix Info Dump ---")
        print(f"Called From Function - {frame_info.f_code.co_name} ({frame_info.f_code.co_filename}) - Line {frame_info.f_lineno}")
        print(f"Timestamp - [{datetime.now().strftime("%H:%M:%S")}]")
        print(f"Matrix Content [{self.dimensions}]\n{self.to_string()}\n")
     
    def to_string(self): # convert matrix to string format with even spacing 
        column_max_length = [] # for each column, lets find the longest number (string wise) and note this down
        for x in range(self.width):
            column_max_length.append(0)
            for y in range(self.height):
                if self.content[x][y] == 0: self.content[x][y] = 0 # i know this line looks stupid, but it converts -(0.0) to 0 in the string
                column_max_length[x] = max(column_max_length[x], len(f"{self.content[x][y]:g}"))
        
        mat_string = "" 
        for y in range(self.height): # now lets create the string
            row_string = "["
            for x in range(self.width):
                row_string += f"{self.content[x][y]:g}"
                row_string += " " * (column_max_length[x] + 1 - len(f"{self.content[x][y]:g}"))
            row_string = row_string[:-1] + "]"
            mat_string += f"{row_string}\n"
        mat_string = mat_string[:-1]
        
        return mat_string
    
    def to_database_format(self): # convert matrix to database string format 1,4,-3.2,3.....
        s = ""
        for x in range(self.width):
            for y in range(self.height):
                s += f"{self.content[x][y]},"
        return s[:-1]
    
    # check if matrix fits a given format e.g "1,0,0,0,xS,yS-,0,yS,xS"
    # numbers require that exact number to be present
    # each seperate variable e.g x and y are assigned the first value found
    # - tells the function to search for negative version of variable
    # S tells the function var must have abs value <= 1 
    def in_format(self, format):
        split_format = format.split(',')
        variables = {}
        
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x #1d index from 2d mat
                try: # assume the number is a float and do a comparision
                    if self.content[x][y] != float(split_format[index]): 
                        return False
                except ValueError: # split_format[index] was not a number, now we do var checks    
                    if 'S' in split_format[index][1:] and abs(self.content[x][y] > 1): 
                        return False
                    
                    var = split_format[index][0] # first index always the variable
                    if var not in variables: # we havent come across this variable yet
                        variables[var] = -self.content[x][y] if '-' in split_format[index][1:] else self.content[x][y]
                    elif -variables[var] if '-' in split_format[index][1:] else variables[var] != self.content[x][y]:
                        return False    
        return True

    # --- Matrix Operations ---

    def scalar_multiply(self, factor): # multiply all cells of matrix by scalar value
        mat = Matrix(self.width, self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                mat.content[x][y] = self.content[x][y] * factor
        
        mat.print()
        return mat
    
    def to_pow(self, factor): # multiply matrix by itself, factor times
        if not self.is_square: 
            return err.raise_error("E110")
        if abs(factor) > 10:
            return err.raise_error("E200") 
        
        if factor == 0: return Matrix.identiy(self.width) # A^0 = I (equivaleint to x^0 = 1) 
        
        mat = Matrix.copy(self)
        for i in range(int(abs(factor) - 1)):
            mat = Matrix.multiply_matrice(mat, self)
            
        if factor < 0: # if negative we take the inverse (like 2^(-1) = 1/2)
            mat = mat.invert()    
            if mat == False: return False
            
        mat.print()
        return mat
    
    def transpose(self): # flips matrix over the diagonal
        mat = Matrix(self.height, self.width)
        for x in range(self.width):
            for y in range(self.height):
                mat.content[y][x] = self.content[x][y]
                
        mat.print()
        return mat
    
    def invert(self): # find the inverse A^(-1) of matrix A such that A * A^(-1) = A^(-1) * A = I
        if not self.is_square:
            return err.raise_error("E111")
        
        det = self.determinant()
        if det == 0:
            return err.raise_error("E101")
        
        mat = Matrix.copy(self)

        if self.width == 1: # matrix is single number 
            mat.content[0][0] = 1/det
            return mat
        
        for x in range(mat.width):
            for y in range(mat.height):
                mat.content[x][y] = (-1)**(x + y) * Matrix.cut(self, x, y).determinant() #get the minor for this part of the matrix
        
        mat = mat.scalar_multiply(1/det)
        mat = mat.transpose()
        
        mat.print()
        return mat
            
            
    def determinant(self): # recursive function to find det
        if not self.is_square:
            return err.raise_error("E112")
        
        if self.width == 1:
            return self.content[0][0]
        
        if self.width == 2: #2 x 2 matrix
            return (self.content[0][0] * self.content[1][1]) - (self.content[0][1] * self.content[1][0])
        
        det = (self.content[0][0] * Matrix.cut(self, 0, 0).determinant() 
            - self.content[1][0] * Matrix.cut(self, 1, 0).determinant() 
            + self.content[2][0] * Matrix.cut(self, 2, 0).determinant())
        if self.width == 4:
            det -= self.content[3][0] * Matrix.cut(self, 3, 0).determinant()
            
        return det
    
    def row_echelon_form(self): #convert matrix to row echelon form (special arrangement)
        mat = Matrix.copy(self)
        pivot_y = 0
        
        for x in range(mat.width):
            nonzero_y = mat.find_non_zero_cell(x, pivot_y)
            if nonzero_y != None:
                mat.swap_rows(pivot_y, nonzero_y)
                mat.cell_below(x, pivot_y)
                pivot_y += 1
        mat.print()
        return mat
    
    def find_non_zero_cell(self, x, pivot_y):
        for y in range(pivot_y, self.height):
            if self.content[x][y] != 0:
                return y
        return None
    
    def cell_below(self, x, pivot_y):
        pivot_element = self.content[x][pivot_y]
        for y in range(pivot_y + 1, self.height):
            factor = self.content[x][y] / pivot_element
            for i in range(self.width):
                self.content[i][y] -= factor * self.content[i][pivot_y]
    
    def rank(self): #find the largest size matrix with a determiant of 0
        mat = self.row_echelon_form() 
        for y in range(mat.height): # find first 0 column
            if mat.content[mat.width - 1][y] == 0: return y
        return y + 1
    
    # --- STATIC TWO MATRIX FUNCTIONS ---
    
    @staticmethod
    def add_subtract_matrice(mat_a: Matrix, mat_b: Matrix, subtract = False): #add or subtract together the two matrice
        if mat_a.width != mat_b.width or mat_a.height != mat_b.height:
            return err.raise_error("E114", "Subtract" if subtract else "Add")
        
        mat_result = Matrix(mat_a.width, mat_a.height)
        for y in range(mat_a.height):
            for x in range(mat_b.width):
                mat_result.content[x][y] = mat_a.content[x][y] + (-mat_b.content[x][y] if subtract else mat_b.content[x][y]) 
                
        mat_result.print()
        return mat_result
    
    @staticmethod
    def multiply_matrice(mat_a: Matrix, mat_b: Matrix): #finds the dot product of two matrice
        if mat_a.width != mat_b.height: #requirement for matrix multiplication
            return err.raise_error("E113")
        
        mat_result = Matrix(mat_b.width, mat_a.height)
        for y in range(mat_a.height): #loop through each row in mat
            for x in range(mat_b.width): #each row must be compared with every column
                cell_total = 0
                for i in range(mat_a.width): #now multiply elements (could also use height of mat_b)
                    cell_total += mat_a.content[i][y] * mat_b.content[x][i]
                mat_result.content[x][y] = cell_total
                
        mat_result.print()
        return mat_result
    
    @staticmethod
    def swap_matrice(mat_a: Matrix, mat_b: Matrix): #swaps the content and size of two matrix
        mat_a.content, mat_b.content = mat_b.content, mat_a.content
        mat_a.set_dimensions(len(mat_a.content), len(mat_a.content[0]))
        mat_b.set_dimensions(len(mat_b.content), len(mat_b.content[0]))
        
    
    
    
                
        
                    
                    
                
        
        
        
        

            
    
                
        
