import pygame

# Board dimensions
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
BOARD_HEIGHT = BOARD_SIZE * SQUARE_SIZE

# Window dimensions
WINDOW_WIDTH = BOARD_WIDTH + 300  # More space for better UI
WINDOW_HEIGHT = BOARD_HEIGHT + 120

# Enhanced Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Beautiful chess board colors
LIGHT_SQUARE = (240, 217, 181)     # Elegant cream
DARK_SQUARE = (181, 136, 99)      # Warm brown
BOARD_BORDER = (139, 69, 19)      # Saddle brown

# Modern UI colors
UI_BACKGROUND = (248, 248, 250)   # Light gray background
UI_PANEL = (255, 255, 255)       # Clean white panels
UI_TEXT = (51, 51, 51)           # Dark gray text
UI_ACCENT = (72, 133, 237)       # Modern blue
UI_SUCCESS = (52, 168, 83)       # Green
UI_WARNING = (251, 188, 5)       # Amber
UI_ERROR = (234, 67, 53)         # Red

# Enhanced game colors
HIGHLIGHT_COLOR = (255, 235, 59, 180)    # Soft yellow highlight
VALID_MOVE_COLOR = (76, 175, 80, 160)    # Gentle green
SELECTED_COLOR = (255, 193, 7, 200)      # Golden selection
LAST_MOVE_COLOR = (156, 39, 176, 120)    # Purple for last move

# Gradient colors for modern look
GRADIENT_START = (245, 245, 245)
GRADIENT_END = (230, 230, 230)

# Piece colors
WHITE_PIECE = 'white'
BLACK_PIECE = 'black'

# Starting positions
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Piece types
PAWN = 'pawn'
ROOK = 'rook'
KNIGHT = 'knight'
BISHOP = 'bishop'
QUEEN = 'queen'
KING = 'king'

# Piece values (for AI evaluation)
PIECE_VALUES = {
    PAWN: 1,
    KNIGHT: 3,
    BISHOP: 3,
    ROOK: 5,
    QUEEN: 9,
    KING: 100
}

# Rendering options
USE_BACKGROUND_CIRCLES = False  # Set to True for background circle rendering, False for outline rendering
USE_ASCII_PIECES = False        # Set to False for Unicode chess symbols, True for ASCII letters

# Font preferences for Unicode support (macOS optimized)
PREFERRED_UNICODE_FONTS = [
    'Apple Symbols',           # Best macOS font for chess symbols
    'Apple Color Emoji',       # Fallback with emoji support
    'SF Pro Display',          # Apple system font
    'Arial Unicode MS',        # Microsoft Unicode font
    'DejaVu Sans',            # Open source Unicode font
    'Menlo',                  # macOS monospace with Unicode
    'Arial',                  # Basic fallback
]

# UI Layout Constants
UI_MARGIN = 20
PANEL_PADDING = 15
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 120
CORNER_RADIUS = 8

# Font sizes
TITLE_FONT_SIZE = 28
SUBTITLE_FONT_SIZE = 20
BODY_FONT_SIZE = 16
SMALL_FONT_SIZE = 12

# Animation settings
PIECE_ANIMATION_SPEED = 8
HIGHLIGHT_PULSE_SPEED = 3
FADE_IN_SPEED = 5

# Board styling
BOARD_SHADOW_OFFSET = 5
PIECE_SCALE = 0.8
HOVER_SCALE = 1.1