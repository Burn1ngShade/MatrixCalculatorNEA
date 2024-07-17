import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matrix import Matrix
import entry_validation as val

class Visual_Window:
    unit_square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    
    def __init__(self, app):
        self.app = app
        
        self.panel = tk.Frame(app.root, bg="snow3")
        self.panel.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.panel.option_add( "*font", "Consolas 8" )
        
        tk.Button(self.panel, text="Exit", width=17, height=1, command=lambda:(self.app.open_window(1))).place(x = 400, y = 20, anchor="center")
        
    def visualise_matrix(self, mat : Matrix):
        if mat.width == 4 or mat.height == 4: return val.raise_error("E200", "4 Dimensional Matrice Can Not Be Visualised. (Only Matrix Of 1x1, 2x2, 3x3, 2x1, 1x2, 3x1 and 1x3 Can Be Visualised).")
        
        self.app.open_window(2)
        
        points = []
        if mat.width == 2 and mat.height == 2:
            for i in range(len(self.unit_square)):
                mat2 = Matrix(1, 2)
                mat2.set_from_values(self.unit_square[i])
                mat_result = Matrix.multiply_matrice(mat, mat2)
                points.append((mat_result.content[0][0], mat_result.content[0][1]))
                
            self.unit_square_visual(self.unit_square, points)
        
    def unit_square_visual(self, points_base, points_transformed):
        fig = Figure(figsize=(7, 7), dpi=100)
        fig.patch.set_facecolor("#cdc9c9")
        graph = fig.add_subplot(111)
        
        overlap = set(points_base) & set(points_transformed)
        
        base_x, base_y = [point[0] for point in points_base], [point[1] for point in points_base]
        trans_x, trans_y = [point[0] for point in points_transformed], [point[1] for point in points_transformed]
        over_x, over_y = [point[0] for point in overlap], [point[1] for point in overlap]

        graph.scatter(base_x, base_y, color="red", label="Unit Square")
        base_x.append(base_x[0]), base_y.append(base_y[0])
        graph.plot(base_x, base_y, color="red")
        graph.scatter(trans_x, trans_y, color = "blue", label="Transformed Unit Square")
        trans_x.append(trans_x[0]), trans_y.append(base_y[0])
        graph.plot(trans_x, trans_y, color="blue")
        graph.scatter(over_x, over_y, color="green", label="Overlapping Points")
        graph.set_title("Matrix Effects On The Unit Square")
        graph.set_xlabel("YO")
        graph.legend(loc="upper right")
        
        print(graph.get_xlim())
        print(graph.get_ylim())
        
        max_limt = max(graph.get_xlim()[1], graph.get_ylim()[1])
        min_limit = min(graph.get_xlim()[0], graph.get_ylim()[0])
        
        graph.set_xlim(min_limit, max_limt)
        graph.set_ylim(min_limit, max_limt)
        
        canvas = FigureCanvasTkAgg(fig, master=self.panel)
        canvas.draw()
        canvas.get_tk_widget().place(x = 400, y = 400, anchor="center")
        
#2x2
#3x3
#2x1
#3x1
#1x2
#1x3 //same way as 3x1
#1x1
        
        