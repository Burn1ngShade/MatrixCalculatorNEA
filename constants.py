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

# databases
DEFAULT_DATABASE_PATH = "Assets/Matrix Calculator Database.db"
MATRIX_CALCULATION_ELEMENT_DB_COLUMNS = ("MatrixCalculationID", "PrefixText", "SuffixText", "MatrixWidth", "MatrixHeight", "MatrixContent")
MATRIX_CALCULATION_DB_COLUMNS = ("UserID", "CreationDate")
USER_DB_COLUMNS = ("Username", "Password")