# DO NOT MODIFY THESE VALUES OUTSIDE THIS SCRIPT

# matrix calculator ui 
MATRIX_X_BASE = 174
MATRIX_REFLECTED_X_BASE = 626 
MATRIX_X_BASE_DIF = 452
MATRIX_Y_BASE = 75

MATRIX_OP_BASE_Y = 183
MATRIX_OP_X_SPACING = 62

# matrix previous calculations UI
MATRIX_CALC_BASE_Y = 390
MATRIX_CALC_INCR_Y = 90
MATRIX_CALC_SORT_OPTIONS = ["Creation Date (Descending)", "Creation Date (Ascending)", "Size (Descending)", "Size (Ascending)", "Rank (Descending)", "Rank (Ascending)"]

# window sizes
WINDOW_GEOMETRY = ["800x525", "800x800", "800x800"]

# visual window
UNIT_SQUARE = [(0, 0), (0, 1), (1, 1), (1, 0)]
UNIT_CUBE = [(0, 0, 0),(0, 0, 1),(0, 1, 1),(0, 1, 0),(1, 1, 0),(1, 1, 1),(1, 0, 1),(1, 0, 0)]
UNIT_CUBE_PLOT_LISTS = [[0, 7, 6, 1], [3, 0, 1, 2], [4, 3, 2, 5], [7, 4, 5, 6]]
VALID_VISUAL_MATRIX_DIMENSIONS = ["1x1", "2x2", "3x3", "1x2", "1x3", "3x1", "2x1"] 
TWO_DIMENSION_MATRIX_TRANSFORMATIONS = ["1x1", "2x2", "1x2", "2x1"]
THREE_DIMENSION_MATRIX_TRANSFORMATION = ["3x3", "1x3", "3x1"]

# account
GUEST_USERNAME = "Guest"

# error handler
ERROR_CODES = {
    # login errors
    "E000" : ("Invalid Username", "Usernames Must Be 5-15 Characters."),
    "E001" : ("Invalid Username", f"Username Can Not Be {GUEST_USERNAME}."),
    "E002" : ("Invalid Username", "Account With Username [x] Does Not Exist."),
    "E003" : ("Invalid Username", "Username Is Already Taken."),
    "E010" : ("Invalid Password", f"Passwords Must Be 5-15 Characters." ),
    "E011" : ("Invalid Password", "Password Is Incorrect."),
    # matrix
    "E100" : ("Invalid Determinant", "Matrice Raised To A Negative Power Can't Have A Determinant Of 0."), 
    "E101" : ("Invalid Determinant", "Matrice With A Determinant Of 0 Can't Be Inverted."), 
    "E110" : ("Invalid Dimensions", "Only Square Matrice Can Be Raised To A Power."),
    "E111" : ("Invalid Dimensions", "Only Square Matrice Can Be Inverted."),
    "E112" : ("Invalid Dimensions", "Only Square Matrice Have Determinants."),
    "E113" : ("Invalid Dimensions", "Matrix A Must Have The Same Number Of Columns As Matrix B Has Rows."),
    "E114" : ("Invalid Dimensions", "Matrix A And Matrix B Must Be The Same Size To [x]."),
    "E115" : ("Invalid Dimensions", "Matrice Of Dimensions [x]x[x] Can Not Be Visualised. Valid Dimensions: 1x1, 2x2, 3x3, 2x1, 1x2, 3x1, 1x3."),
    # math error
    "E200" : ("Out Of Range", "Powers Must Range Between -10 and 10.")        
}

# databases
DEFAULT_DATABASE_PATH = "Assets/Matrix Calculator Database.db"
MATRIX_CALCULATION_ELEMENT_DB_COLUMNS = ("MatrixCalculationID", "PrefixText", "SuffixText", "MatrixWidth", "MatrixHeight", "MatrixContent")
MATRIX_CALCULATION_DB_COLUMNS = ("UserID", "CreationDate")
USER_DB_COLUMNS = ("Username", "Password")