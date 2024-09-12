import math
import tkinter as tk
import constants as c
import matplotlib.pyplot as plt
from matrix import Matrix
from window import Window
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from error_handler import Error_Handler as err

class Visual_Window(Window):
    def __init__(self, app):     
        super().__init__(app)
        
    # --- SETUP ---    
        
    def setup_window(self): # draw and setup all elements in window    
        self.setup_matplotlib()
        self.setup_info_buttons()
        
    def setup_matplotlib(self): # setup matplotlib and graph
        # set up matplotlibs graphing settings to be the same as ours
        plt.rcParams['font.family'] = 'Consolas'
        plt.rcParams['font.size'] = 12
        plt.rcParams['font.weight'] = 'ultralight'
        
        # set up our graph
        self.fig = Figure(figsize=(6.7, 6.7), dpi=100)
        self.fig.patch.set_facecolor("#CDC9C9")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel)
    
    def setup_info_buttons(self): # setup background and buttons info
        # frames
        bot_info_frame = tk.Frame(self.panel, bg="gainsboro", width=800, height=150)
        bot_info_frame.place(x=400, y=800, anchor="s")
        right_info_frame = tk.Frame(self.panel, bg="snow3", width=190, height=620)
        right_info_frame.place(x=800, y=0, anchor="ne")
        
        # buttons
        self.matrix_label = tk.Label(bot_info_frame, bg="gainsboro", text="Visualising Matrix:")
        self.matrix_label.place(x=150, y=0, anchor="n")
        self.matrix_info_label = tk.Label(bot_info_frame, bg="gainsboro", text="Matrix Info:")
        self.matrix_info_label.place(x = 650, y =0, anchor="n")
        self.point_text = tk.Label(right_info_frame, bg="gainsboro", anchor="w", justify="left", width=100)
        self.point_text.place(x = 0, y = 143, anchor="nw")
        self.identify_text = tk.Label(bot_info_frame, bg="gainsboro", width=100, text="Transformation Details:")
        self.identify_text.place(x=400, y=100, anchor="n")
        tk.Button(bot_info_frame, text="Exit", width=17, height=1, command=lambda:(self.app.open_window(1))).place(x = 400, y = 10, anchor="n")
        
        # legend
        self.legend_text = tk.Label(right_info_frame, bg="gainsboro", anchor="w", justify="left", width=100)
        self.legend_text.place(x=0, y=60, anchor="nw")
        self.legend_text.config(text="  Base Points\n  Transformed Points\n  Overlap") 
        
        legend_canvas = Canvas(right_info_frame, width=15, height=59, bg="gainsboro", highlightbackground="gainsboro")
        legend_canvas.place(x = 0, y = 60, anchor="nw")
        legend_canvas.create_rectangle(5, 8, 15, 18, fill="red")
        legend_canvas.create_rectangle(5, 27, 15, 37, fill="blue")
        legend_canvas.create_rectangle(5, 46, 15, 56, fill="green")
        
    # --- VISUALISE FUNCTIONS ---
        
    def visualise_matrix_transformation(self, mat : Matrix): # visualises matrix and the transformation it represents    
        if mat.dimensions not in c.VALID_VISUAL_MATRIX_DIMENSIONS: # not all matrice represent a transformation
            return err.raise_error("E115", [mat.height, mat.width])
            
        # update information ui
        self.app.open_window(2) # open window
        self.identify_text.config(text=f"Transformation Details:\n{self.identify_matrix_transformation(mat)}") # type of transformation
        self.matrix_label.config(text=f"Visualising Matrix:\n{mat.to_string()}") # matrix thats being visualised
        self.matrix_info_label.config(text=f"Matrix Info:\nDimensions - {mat.dimensions}\nRank - {mat.rank()}") # matrix info
        
        points = []
        if mat.dimensions in c.TWO_DIMENSION_MATRIX_TRANSFORMATIONS: # matrix represents a 2d transformation
            for point in c.UNIT_SQUARE: # 1 x 1 square at the origin
                point_mat = Matrix(1, 2) 
                point_mat.set_from_list(point)
            
                if mat.dimensions == "1x1":
                    point_mat = point_mat.scalar_multiply(mat.content[0][0])
                    points.append((point_mat.content[0][0], point_mat.content[0][1]))    
                elif mat.dimensions == "1x2":
                    point_mat = Matrix.multiply_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], 0))
                elif mat.dimensions == "2x1":
                    point_mat = Matrix.add_subtract_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], point_mat.content[0][1]))
                elif mat.dimensions == "2x2":
                    point_mat = Matrix.multiply_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], point_mat.content[0][1]))
                    
            self.graph_points_against_unit_square(c.UNIT_SQUARE, points)
            
        elif mat.dimensions in c.THREE_DIMENSION_MATRIX_TRANSFORMATION: # matrix represents a 3d transformation
            for point in c.UNIT_CUBE: # 1 x 1 x 1 cube at the origin
                point_mat = Matrix(1, 3)
                point_mat.set_from_list(point)
                
                if mat.dimensions == "1x3":
                    point_mat = Matrix.multiply_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], 0, 0))
                elif mat.dimensions == "3x1":
                    point_mat = Matrix.add_subtract_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], point_mat.content[0][1], point_mat.content[0][2]))
                elif mat.dimensions == "3x3":
                    point_mat = Matrix.multiply_matrice(mat, point_mat)
                    points.append((point_mat.content[0][0], point_mat.content[0][1], point_mat.content[0][2]))
                    
            self.graph_points_against_unit_cube(c.UNIT_CUBE, points)
        
    def graph_points_against_unit_square(self, base_points, trans_points): # graph a set of 2d points and the unit square
        # set up graph for 2d rendering
        self.fig.clear()
        graph = self.fig.add_subplot(111)
        graph.set_facecolor("#DCDCDC") #set foreground to gainsboro
        graph.grid(True, zorder=0) #gridlines 
        graph.set_title("Effects Of Matrix On The Unit Square")
        self.canvas.get_tk_widget().place(x = -10, y = -20, anchor="nw")
        
        # update ui
        base_point_text = "Orignal Points:\n" + '\n'.join(f"({p[0]}, {p[1]})" for p in base_points) + "\n\n"
        trans_point_text = "Transformed Points:\n" + '\n'.join(f"({p[0]:g}, {p[1]:g})" for p in trans_points)
        self.point_text.config(text=base_point_text + trans_point_text)
        
        # convert from lists of points to two seperate lists of floats
        overlap_points = list(set(base_points) & set(trans_points)) # find all overlapping points

        filtered_base_points = list(zip(*(p for p in base_points if p not in overlap_points))) #create version of base points exc overlaps
        filtered_trans_points = list(zip(*(p for p in trans_points if p not in overlap_points))) # create version of trans points exc overlaps

        # convert from a list (x, y) to a tuple with a x list and a y list
        overlap_points = list(zip(*(set(base_points) & set(trans_points))))
        base_points = list(zip(*base_points)) 
        trans_points = list(zip(*trans_points))
        
        # now lets place points onto the graph
        if (len(filtered_base_points) > 0): graph.scatter(filtered_base_points[0], filtered_base_points[1], color="red", zorder=5) # base points
        if (len(filtered_trans_points) > 0): graph.scatter(filtered_trans_points[0], filtered_trans_points[1], color="blue", zorder=6) # transformed points
        if (len(overlap_points) > 0): graph.scatter(overlap_points[0], overlap_points[1], color="green", zorder=7) # overlap points
        
        # add additional point repeats
        base_points[0] += (base_points[0][0],)
        base_points[1] += (base_points[1][0],)
        trans_points[0] += (trans_points[0][0],)
        trans_points[1] += (trans_points[1][0],)
        
        # overlapping lines - as we are always using the unit square we can skip any complicated gradient and overlap maths and just check the four lines making up the unit square
        for i in range(len(base_points[0]) - 1):
            tp = (trans_points[0][i], trans_points[1][i])  
            tp_next = (trans_points[0][i + 1], trans_points[1][i + 1])
            
            if tp_next[1] == tp[1] and (tp[1] == 0 or tp[1] == 1): # horizontal line
                if max(tp[0], tp_next[0]) < 0 or min(tp[0], tp_next[0]) > 1: continue
                graph.plot([max(0, min(tp[0], tp_next[0])), min(1, max(tp[0], tp_next[0]))], [tp[1], tp[1]], color="green", zorder=4)
            if tp_next[0] == tp[0] and (tp[0] == 0 or tp[0] == 1): # vertical line
                if max(tp[1], tp_next[1]) < 0 or min(tp[1], tp_next[1]) > 1: continue
                graph.plot([tp[0], tp[0]], [max(0, min(tp[1], tp_next[1])), min(1, max(tp[1], tp_next[1]))], color="green", zorder=4)
        
        # now lets place lines onto graph
        graph.plot(base_points[0], base_points[1], color="red", zorder=2)
        graph.plot(trans_points[0], trans_points[1], color="blue", zorder=3)
        
        # lets set graph x and y limits to be the same to prevent stretching
        min_limit, max_limit = min(graph.get_xlim()[0], graph.get_ylim()[0]), max(graph.get_xlim()[1], graph.get_ylim()[1])
        graph.set_xlim(min_limit, max_limit)
        graph.set_ylim(min_limit, max_limit)
        
        self.canvas.draw() #update canvas with grid

    def graph_points_against_unit_cube(self, base_points, trans_points): # graph a set of 3d points and the unit cube
        # set up graph for 3d rendering
        self.fig.clear()
        graph = self.fig.add_subplot(111, projection="3d")
        graph.set_facecolor("#DCDCDC") #set foreground to gainsboro
        graph.grid(True, zorder=0) #gridlines 
        graph.set_title("Effects Of Matrix On The Unit Cube")
        self.canvas.get_tk_widget().place(x = -50, y = -20, anchor="nw")
        
        # update ui
        base_point_text = "Orignal Points:\n" + '\n'.join(f"({p[0]}, {p[1]}, {p[2]})" for p in base_points) + "\n\n"
        trans_point_text = "Transformed Points:\n" + '\n'.join(f"({p[0]:g}, {p[1]:g}, {p[2]:g})" for p in trans_points)
        self.point_text.config(text=base_point_text + trans_point_text)

        
        # convert from lists of points to two seperate lists of floats
        overlap_points = list(set(base_points) & set(trans_points)) # find all overlapping points

        filtered_base_points = list(zip(*(p for p in base_points if p not in overlap_points))) #create version of base points exc overlaps
        filtered_trans_points = list(zip(*(p for p in trans_points if p not in overlap_points))) # create version of trans points exc overlaps

        # convert from a list (x, y) to a tuple with a x list and a y list
        overlap_points = list(zip(*(set(base_points) & set(trans_points))))
        base_points = list(zip(*base_points)) 
        trans_points = list(zip(*trans_points))

        if (len(filtered_base_points) > 0): graph.scatter(filtered_base_points[0], filtered_base_points[1], filtered_base_points[2], color="red", zorder=5)
        if (len(filtered_trans_points) > 0): graph.scatter(filtered_trans_points[0], filtered_trans_points[1], filtered_trans_points[2], color="blue", zorder=6)
        if (len(overlap_points) > 0): graph.scatter(overlap_points[0], overlap_points[1], overlap_points[2], color="green", zorder=7)

        # place lines onto the graph (logic is alot more complex for 3d)
        for plot in c.UNIT_CUBE_PLOT_LISTS:
            # overlapping lines - as we are always using the unit cube we can skip any complicated gradient and overlap maths and just check the eight lines making up the unit cube
            
            for i in range(len(plot) - 1):
                tp = (trans_points[0][plot[i]], trans_points[1][plot[i]], trans_points[2][plot[i]])  
                tp_next = (trans_points[0][plot[i + 1]], trans_points[1][plot[i + 1]], trans_points[2][plot[i + 1]])

                if tp_next[1] == tp[1] and tp_next[2] == tp[2] and (tp[1] == 0 or tp[1] == 1) and (tp[2] == 0 or tp[2] == 1): # horizontal line
                    if max(tp[0], tp_next[0]) < 0 or min(tp[0], tp_next[0]) > 1: continue
                    graph.plot([max(0, min(tp[0], tp_next[0])), min(1, max(tp[0], tp_next[0]))], [tp[1], tp[1]], [tp[2], tp[2]], color="green", zorder=4)
                if tp_next[0] == tp[0] and tp_next[2] == tp[2] and (tp[0] == 0 or tp[0] == 1) and (tp[2] == 0 or tp[2] == 1): # other horizontal line
                    if max(tp[1], tp_next[1]) < 0 or min(tp[1], tp_next[1]) > 1: continue
                    graph.plot([tp[0], tp[0]], [max(0, min(tp[1], tp_next[1])), min(1, max(tp[1], tp_next[1]))], [tp[2], tp[2]], color="green", zorder=4)
                if tp_next[0] == tp[0] and tp_next[1] == tp[1] and (tp[0] == 0 or tp[0] == 1) and (tp[1] == 0 or tp[1] == 1): # vertical line
                    if max(tp[2], tp_next[2]) < 0 or min(tp[2], tp_next[2]) > 1: continue
                    graph.plot([tp[0], tp[0]], [tp[1], tp[1]], [max(0, min(tp[2], tp_next[2])), min(1, max(tp[2], tp_next[2]))], color="green", zorder=4)
            

            # normal plots
            graph.plot([base_points[0][i] for i in plot], [base_points[1][i] for i in plot], [base_points[2][i] for i in plot], color="red", zorder=2)
            graph.plot([trans_points[0][i] for i in plot], [trans_points[1][i] for i in plot], [trans_points[2][i] for i in plot], color="blue", zorder=3)

        # lets set graph x and y and z limits to be the same to stop stretching
        min_limit, max_limit = min(graph.get_xlim()[0], min(graph.get_ylim()[0], graph.get_zlim()[0])), max(graph.get_xlim()[1], max(graph.get_ylim()[1], graph.get_zlim()[1]))
        graph.set_xlim(min_limit, max_limit)
        graph.set_ylim(min_limit, max_limit)
        graph.set_zlim(min_limit, max_limit)

        self.canvas.draw() #update canvas with grid
        
    def identify_matrix_transformation(self, mat : Matrix): # identify the type of transformation a matrix represents
        if mat.dimensions == "1x1":
            return f"Scalar Multiplication By Scale Factor {mat.content[0][0]:g}"
        elif mat.dimensions == "2x1":
            return f"Translation Of A 2D Point By Vector ({mat.content[0][0]:g}, {mat.content[0][1]:g})"
        elif mat.dimensions == "1x2":
            return f"Dot Product Of Matrix And Unit Square"
        elif mat.dimensions == "3x1":
            return f"Translation Of A 3D Point By Vector ({mat.content[0][0]:g}, {mat.content[0][1]:g}, {mat.content[0][2]:g})"
        elif mat.dimensions == "1x3":
            return f"Dot Product Of Matrix And Unit Cube"
        elif mat.dimensions == "2x2":
            if mat.is_identity: return f"Identity Matrix (No Effect)"
            
            # is the matrix a rotation
            if (mat.in_format("xS,yS-,yS,xS")):
                theta_cos = math.acos(mat.content[0][0])
                theta_sin = math.asin(mat.content[0][1])
                if math.isclose(math.cos(theta_cos), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_cos), mat.content[0][1], abs_tol=0.001):
                    return f"Anticlockwise Rotation By {round(math.degrees(theta_cos), 2):g} Degrees"
                elif math.isclose(math.cos(theta_sin), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_sin), mat.content[0][1], abs_tol=0.001):
                    return f"Anticlockwise Rotation By {round(math.degrees(theta_sin), 2):g} Degrees"
                
            # is the matrix a reflection
            if (mat.in_format("xS-,yS,yS,xS")):
                theta_cos = math.acos(mat.content[0][0])
                theta_sin = math.asin(mat.content[0][1])
                print(theta_cos, theta_sin)
                if math.isclose(math.cos(theta_cos), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_cos), mat.content[0][1], abs_tol=0.001):
                    return f"Reflection In The Line y = {round(math.tan(theta_cos / 2), 2):g}x"
                elif math.isclose(math.cos(theta_sin), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_sin), mat.content[0][1], abs_tol=0.001):
                    return f"Reflection In The Line y = {round(math.tan(theta_sin / 2), 2):g}x"
            
            # no special case found (covered under a level further math spec), so we can just describe it as a scaling and shearing process
            scale_shear = ""
            if (mat.content[0][0] == 0 or mat.content[1][1] == 0) and (mat.content[0][1] != 0 or mat.content[1][0] != 0):
                return "Mix Of Scaling And Shearing (Unidentifiable)"
            if mat.content[0][1] != 0 or mat.content[1][0] != 0:
                scale_shear += f"Sheared By Factor ({(mat.content[1][0] / mat.content[0][0]):g}, {(mat.content[0][1] / mat.content[1][1]):g}) " 
            if mat.content[0][0] != 1 or mat.content[1][1] != 1:
                if len(scale_shear) > 0: scale_shear += "Then "
                scale_shear += f"Stretched By Scale Factor ({mat.content[0][0]:g}, {mat.content[1][1]:g}) "    
            return scale_shear if len(scale_shear) > 0 else "Mix Of Scaling And Shearing (Unidentifiable)" 
        elif mat.dimensions == "3x3":
            if mat.is_identity: return f"Identity Matrix (No Effect)"
            
            # rotation
            if mat.in_format("1,0,0,0,xS,yS-,0,yS,xS"): #rotation around x axis
                theta_cos = math.acos(mat.content[1][1])
                theta_sin = math.asin(mat.content[1][2])
                if math.isclose(math.cos(theta_cos), mat.content[1][1], abs_tol=0.001) and math.isclose(math.sin(theta_cos), mat.content[1][2], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The X Axis By {round(math.degrees(theta_cos), 2):g} Degrees"
                elif math.isclose(math.cos(theta_sin), mat.content[1][1], abs_tol=0.001) and math.isclose(math.sin(theta_sin), mat.content[1][2], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The X Axis By {round(math.degrees(theta_sin), 2):g} Degrees"
            
            if mat.in_format("xS,0,yS,0,1,0,yS-,0,xS"): #rotation around y axis
                theta_cos = math.acos(mat.content[0][0])
                theta_sin = math.asin(mat.content[2][0])
                print("yo")
                if math.isclose(math.cos(theta_cos), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_cos), mat.content[2][0], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The Y Axis By {round(math.degrees(theta_cos), 2):g} Degrees"
                elif math.isclose(math.cos(theta_sin), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_sin), mat.content[2][0], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The Y Axis By {round(math.degrees(theta_sin), 2):g} Degrees"
                
            if mat.in_format("xS,yS-,0,yS,xS,0,0,0,1"): #rotation around y axis
                theta_cos = math.acos(mat.content[0][0])
                theta_sin = math.asin(mat.content[0][1])
                print("yo")
                if math.isclose(math.cos(theta_cos), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_cos), mat.content[0][1], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The Z Axis By {round(math.degrees(theta_cos), 2):g} Degrees"
                elif math.isclose(math.cos(theta_sin), mat.content[0][0], abs_tol=0.001) and math.isclose(math.sin(theta_sin), mat.content[0][1], abs_tol=0.001):
                    return f"Anticlockwise Rotation Through The Z Axis By {round(math.degrees(theta_sin), 2):g} Degrees"
            
            # not rotation so a we try describe it as a mix of scaling and shearing
            scale_shear = ""
            if not mat.in_format("a,0,0,0,b,0,0,0,c"):
                scale_shear += f"Shearing (Unidentifiable) "
            if not mat.in_format("1,a,b,c,1,d,e,f,1"):
                if len(scale_shear) > 0: scale_shear += "Then "
                scale_shear += f"Stretched By Scale Factor ({mat.content[0][0]:g}, {mat.content[1][1]:g}, {mat.content[2][2]:g})"
                
            return scale_shear
        
        
