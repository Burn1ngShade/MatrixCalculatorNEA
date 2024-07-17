from __future__ import annotations
from tkinter import messagebox
import inspect

#base class for matrix representation
class Matrix:
    ERROR_CODE = "E000" #extremely long random number that can be used as a error code
    
    # constructors
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        
        self.set(0)
        
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
    
    # functions
    
    def is_square(self): # returns if the matrix is square or not
        return self.width == self.height
        
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

    # single matrix methods

    def scalar_multiply(self, factor):
        mat_result = Matrix(self.width, self.height)
        
        for y in range(self.height):
            for x in range(self.width):
                mat_result.content[x][y] = self.content[x][y] * factor
        
        mat_result.print()
        return mat_result
    
    def to_pow(self, factor):
        if not self.is_square(): 
            messagebox.showinfo("Invalid Calculation", "Only Square Matrice Can Be Raised To A Power.")
            return Matrix.ERROR_CODE #can only power square matrice    
    
        if abs(factor) > 10: 
            messagebox.showinfo("Invalid Calculation", "Powers Must Range Between -10 and 10.")
            return Matrix.ERROR_CODE #computation will just take 2 long
        
        if factor == 0: return Matrix.identiy(self.width) # A^0 = I (list x^0 = 1)
        
        mat_result = Matrix.copy(self)
        for i in range(int(abs(factor) - 1)):
            mat_result = Matrix.multiply_matrice(mat_result, self)
            
        if factor < 0:
            mat_result_invert = mat_result.invert()    
            if mat_result_invert == Matrix.ERROR_CODE: return Matrix.ERROR_CODE
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
        if not self.is_square():
            messagebox.showinfo("Invalid Calculation", "Only Square Matrice Can Be Inverted.")
            return Matrix.ERROR_CODE
        
        det = self.det()
        if det == 0:
            messagebox.showinfo("Invalid Calculation", "Matrice With A Determinant Of 0 Can't Be Inverted.")
            return Matrix.ERROR_CODE
        
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
        if not self.is_square():
            messagebox.showinfo("Invalid Calculation", "Only Square Matrice Have Determinants.")
            return Matrix.ERROR_CODE
        
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
            
    def rank(self): #find the largest matrix with a det of 0
        print("RANK")
        return 0
    
    def row_echelon_form(self):
        re_mat = Matrix.copy(self)
        pivot_row = 0
        
        for x in range(re_mat.width):
            # find non zero row
            for y in range(pivot_row, re_mat.height):
                if re_mat.content[x][y] != 0:
                    # swap row
                    re_mat.print()
                    
                    re_mat.print()
                    # make pibot one
                    # eliminate bloew
                    pivot_row += 1
                    
                    break
                
        return re_mat
        
        
        
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
            messagebox.showinfo("Invalid Calculation", "Matrix A Must Have The Same Number Of Columns As Matrix B Has Rows.")
            return Matrix.ERROR_CODE
        
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
    def add_sub_matrice(mat_a: Matrix, mat_b: Matrix, subtract = False): #add or sub together the scalar values of two matrix
        if mat_a.width != mat_b.width or mat_a.height != mat_b.height:
            messagebox.showinfo("Invalid Calculation", "Both Matrice Must Be The Same Size.")
            return Matrix.ERROR_CODE
        
        mat_result = Matrix(mat_a.width, mat_a.height) #same dimensions
        
        for y in range(mat_a.height):
            for x in range(mat_b.width):
                mat_result.content[x][y] = mat_a.content[x][y] + (-mat_b.content[x][y] if subtract else mat_b.content[x][y]) 
                
        mat_result.print()
        return mat_result
                
        
                    
                    
                
        
        
        
        

            
    
                
        
