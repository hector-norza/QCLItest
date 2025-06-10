import pygame
import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.animation_time = 0
        
        # Load fonts with fallbacks
        self.unicode_supported = False
        self.piece_font = None
        
        # Try fonts known to support Unicode chess symbols (macOS optimized)
        chess_fonts = [
            'Apple Symbols',         # macOS system font with excellent symbol support
            'Arial Unicode MS',      # Available on macOS
            'Lucida Grande',         # macOS default with Unicode support
            'SF Pro Display',        # Apple's system font
            'Helvetica',             # macOS standard
            'DejaVu Sans',           # If installed via Homebrew
            'Noto Sans',             # Google's Unicode font
            'Times New Roman',       # Fallback with some Unicode
            'Arial',                 # Basic fallback
        ]
        
        # Test each font for Unicode chess symbol support
        for font_name in chess_fonts:
            try:
                test_font = pygame.font.SysFont(font_name, 24, bold=True)
                if test_font:
                    # Test if it can render chess symbols properly
                    test_surface = test_font.render('♔', True, (255, 255, 255))
                    if test_surface.get_width() > 10:  # If it renders with reasonable width
                        # This font works! Use it for all text
                        self.title_font = pygame.font.SysFont(font_name, TITLE_FONT_SIZE, bold=True)
                        self.subtitle_font = pygame.font.SysFont(font_name, SUBTITLE_FONT_SIZE, bold=True)
                        self.body_font = pygame.font.SysFont(font_name, BODY_FONT_SIZE)
                        self.small_font = pygame.font.SysFont(font_name, SMALL_FONT_SIZE)
                        self.piece_font = pygame.font.SysFont(font_name, int(SQUARE_SIZE * 0.8), bold=True)
                        self.unicode_supported = True
                        print(f"✅ Unicode chess symbols supported with font: {font_name}")
                        break
            except:
                continue
        
        # Fallback if no Unicode support found
        if not self.unicode_supported:
            print("⚠️  Unicode chess symbols not supported, using ASCII letters")
            try:
                self.title_font = pygame.font.SysFont('Arial', TITLE_FONT_SIZE, bold=True)
                self.subtitle_font = pygame.font.SysFont('Arial', SUBTITLE_FONT_SIZE, bold=True)
                self.body_font = pygame.font.SysFont('Arial', BODY_FONT_SIZE)
                self.small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE)
                self.piece_font = pygame.font.SysFont('Arial', int(SQUARE_SIZE * 0.8), bold=True)
            except:
                # Final fallback to default font
                self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
                self.subtitle_font = pygame.font.Font(None, SUBTITLE_FONT_SIZE)
                self.body_font = pygame.font.Font(None, BODY_FONT_SIZE)
                self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
                self.piece_font = pygame.font.Font(None, int(SQUARE_SIZE * 0.8))
        
        # ASCII piece symbols for maximum compatibility
        self.piece_symbols = {
            (WHITE_PIECE, KING): '♔',
            (WHITE_PIECE, QUEEN): '♕',
            (WHITE_PIECE, ROOK): '♖',
            (WHITE_PIECE, BISHOP): '♗',
            (WHITE_PIECE, KNIGHT): '♘',
            (WHITE_PIECE, PAWN): '♙',
            (BLACK_PIECE, KING): '♚',
            (BLACK_PIECE, QUEEN): '♛',
            (BLACK_PIECE, ROOK): '♜',
            (BLACK_PIECE, BISHOP): '♝',
            (BLACK_PIECE, KNIGHT): '♞',
            (BLACK_PIECE, PAWN): '♟',
        }
        
        # Fallback ASCII letters (used when Unicode doesn't work)
        self.fallback_ascii_symbols = {
            (WHITE_PIECE, KING): 'K',
            (WHITE_PIECE, QUEEN): 'Q',
            (WHITE_PIECE, ROOK): 'R',
            (WHITE_PIECE, BISHOP): 'B',
            (WHITE_PIECE, KNIGHT): 'N',
            (WHITE_PIECE, PAWN): 'P',
            (BLACK_PIECE, KING): 'k',
            (BLACK_PIECE, QUEEN): 'q',
            (BLACK_PIECE, ROOK): 'r',
            (BLACK_PIECE, BISHOP): 'b',
            (BLACK_PIECE, KNIGHT): 'n',
            (BLACK_PIECE, PAWN): 'p',
        }
        
        # Create surfaces for smooth rendering
        self.board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.ui_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def get_piece_symbol(self, piece):
        """Get the appropriate piece symbol based on font support"""
        # If we have Unicode support and it's enabled, use Unicode symbols
        if not USE_ASCII_PIECES and self.unicode_supported:
            return self.piece_symbols.get((piece.color, piece.get_piece_type()), '?')
        else:
            # Use ASCII letters as fallback
            return self.fallback_ascii_symbols.get((piece.color, piece.get_piece_type()), '?')
    
    def draw_gradient_background(self):
        """Draw beautiful gradient background"""
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(GRADIENT_START[0] * (1 - ratio) + GRADIENT_END[0] * ratio)
            g = int(GRADIENT_START[1] * (1 - ratio) + GRADIENT_END[1] * ratio)
            b = int(GRADIENT_START[2] * (1 - ratio) + GRADIENT_END[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def draw_board(self, board):
        """Draw the chess board with beautiful styling"""
        # Calculate board position (centered with shadow)
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        # Draw board shadow for depth
        shadow_rect = pygame.Rect(
            board_x + BOARD_SHADOW_OFFSET, 
            board_y + BOARD_SHADOW_OFFSET, 
            BOARD_WIDTH, 
            BOARD_HEIGHT
        )
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect)
        
        # Draw board border
        border_rect = pygame.Rect(board_x - 3, board_y - 3, BOARD_WIDTH + 6, BOARD_HEIGHT + 6)
        pygame.draw.rect(self.screen, BOARD_BORDER, border_rect, 3, CORNER_RADIUS)
        
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Calculate square position
                x = board_x + col * SQUARE_SIZE
                y = board_y + row * SQUARE_SIZE
                
                # Draw square with slight rounding
                square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, square_rect)
                
                # Add subtle inner shadow for depth
                pygame.draw.line(self.screen, tuple(max(0, c-20) for c in color), 
                               (x, y), (x + SQUARE_SIZE, y), 1)
                pygame.draw.line(self.screen, tuple(max(0, c-20) for c in color), 
                               (x, y), (x, y + SQUARE_SIZE), 1)
                
                # Highlight selected square with animation
                if board.selected_position == (row, col):
                    # Animated pulse effect
                    pulse = abs(math.sin(self.animation_time * HIGHLIGHT_PULSE_SPEED))
                    alpha = int(100 + 80 * pulse)
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((*SELECTED_COLOR[:3], alpha))
                    self.screen.blit(highlight_surface, (x, y))
                    
                    # Border highlight
                    pygame.draw.rect(self.screen, UI_ACCENT, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Highlight valid moves with gentle glow
                if (row, col) in board.valid_moves:
                    center_x = x + SQUARE_SIZE // 2
                    center_y = y + SQUARE_SIZE // 2
                    
                    # Outer glow
                    glow_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    glow_surface.fill((*VALID_MOVE_COLOR[:3], 60))
                    self.screen.blit(glow_surface, (x, y))
                    
                    # Center dot
                    pygame.draw.circle(self.screen, UI_SUCCESS, (center_x, center_y), 8)
                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 6)
    
    def draw_pieces(self, board):
        """Draw all pieces on the board with enhanced styling"""
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece:
                    # Add slight hover effect for better interactivity
                    scale = PIECE_SCALE
                    if board.selected_position == (row, col):
                        scale = HOVER_SCALE
                    
                    if USE_BACKGROUND_CIRCLES:
                        self.draw_piece_with_background(piece, row, col, board_x, board_y, scale)
                    else:
                        self.draw_piece(piece, row, col, board_x, board_y, scale)
    
    def draw_piece(self, piece, row, col, board_x=0, board_y=0, scale=1.0):
        """Draw a single piece with enhanced styling"""
        x = board_x + col * SQUARE_SIZE
        y = board_y + row * SQUARE_SIZE
        
        # Use text symbols for pieces
        symbol = self.get_piece_symbol(piece)
        
        # Make white pieces solid white and black pieces solid black for better contrast
        if piece.is_white():
            text_color = WHITE
            outline_color = BLACK
        else:
            text_color = BLACK
            outline_color = WHITE
        
        # Scale font for effects
        font_size = int(SQUARE_SIZE * 0.8 * scale)
        if self.unicode_supported and self.piece_font:
            # Use the Unicode-supporting font we found
            try:
                scaled_font = pygame.font.SysFont(self.piece_font.get_ascent(), font_size, bold=True)
            except:
                scaled_font = self.piece_font
        else:
            # Fallback font
            try:
                scaled_font = pygame.font.SysFont('Arial', font_size, bold=True)
            except:
                scaled_font = pygame.font.Font(None, font_size)
        
        # Create outline effect for better visibility
        outline_positions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2
        
        # Draw outline
        for dx, dy in outline_positions:
            outline_surface = scaled_font.render(symbol, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(center_x + dx, center_y + dy))
            self.screen.blit(outline_surface, outline_rect)
        
        # Draw main piece on top
        text_surface = scaled_font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_piece_with_background(self, piece, row, col, board_x=0, board_y=0, scale=1.0):
        """Alternative method: Draw piece with colored background for maximum contrast"""
        x = board_x + col * SQUARE_SIZE
        y = board_y + row * SQUARE_SIZE
        
        # Use text symbols for pieces
        symbol = self.get_piece_symbol(piece)
        
        # Define colors
        if piece.is_white():
            bg_color = WHITE
            text_color = BLACK
            border_color = UI_ACCENT
        else:
            bg_color = BLACK
            text_color = WHITE
            border_color = UI_ACCENT
        
        # Calculate piece area (smaller than full square)
        piece_size = int(SQUARE_SIZE * 0.8 * scale)
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2
        
        # Draw background circle for piece with shadow
        shadow_offset = 2
        pygame.draw.circle(self.screen, (0, 0, 0, 30), 
                          (center_x + shadow_offset, center_y + shadow_offset), piece_size // 2)
        pygame.draw.circle(self.screen, bg_color, (center_x, center_y), piece_size // 2)
        pygame.draw.circle(self.screen, border_color, (center_x, center_y), piece_size // 2, 2)
        
        # Scale font for effects
        font_size = int(SQUARE_SIZE * 0.6 * scale)
        try:
            # Try fonts that support Unicode chess symbols
            scaled_font = pygame.font.SysFont('DejaVu Sans', font_size, bold=True)
        except:
            try:
                scaled_font = pygame.font.SysFont('Arial Unicode MS', font_size, bold=True)
            except:
                try:
                    scaled_font = pygame.font.SysFont('Lucida Grande', font_size, bold=True)
                except:
                    scaled_font = pygame.font.Font(None, font_size)
        
        # Draw piece symbol
        text_surface = scaled_font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_ui(self, board):
        """Draw beautiful game UI elements"""
        # Calculate panel position
        panel_x = BOARD_WIDTH + UI_MARGIN * 2
        panel_y = UI_MARGIN
        panel_width = WINDOW_WIDTH - panel_x - UI_MARGIN
        panel_height = 200
        
        # Draw main UI panel with rounded corners
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.draw_rounded_rect(self.screen, UI_PANEL, panel_rect, CORNER_RADIUS)
        self.draw_rounded_rect(self.screen, UI_ACCENT, panel_rect, CORNER_RADIUS, 2)
        
        # Game title
        title_text = "Chess Game"
        title_surface = self.title_font.render(title_text, True, UI_TEXT)
        title_rect = title_surface.get_rect(centerx=panel_x + panel_width // 2, y=panel_y + PANEL_PADDING)
        self.screen.blit(title_surface, title_rect)
        
        # Current player with color indicator
        player_y = title_rect.bottom + 20
        player_text = f"Current Player:"
        player_surface = self.subtitle_font.render(player_text, True, UI_TEXT)
        self.screen.blit(player_surface, (panel_x + PANEL_PADDING, player_y))
        
        # Player color indicator
        indicator_x = panel_x + PANEL_PADDING + player_surface.get_width() + 10
        indicator_color = WHITE if board.current_player == 'white' else BLACK
        border_color = BLACK if board.current_player == 'white' else WHITE
        
        pygame.draw.circle(self.screen, indicator_color, (indicator_x + 15, player_y + 12), 12)
        pygame.draw.circle(self.screen, border_color, (indicator_x + 15, player_y + 12), 12, 2)
        
        # Game status
        status_y = player_y + 35
        if hasattr(board, 'game_status'):
            status_text = board.game_status
            status_color = UI_SUCCESS if "wins" in status_text else UI_TEXT
        else:
            status_text = "Game in progress"
            status_color = UI_TEXT
            
        status_surface = self.body_font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (panel_x + PANEL_PADDING, status_y))
        
        # Draw controls panel
        controls_y = panel_y + panel_height + 20
        self.draw_controls_panel(panel_x, controls_y, panel_width)
        
        # Draw coordinates
        self.draw_coordinates()
    
    def draw_controls_panel(self, x, y, width):
        """Draw the controls panel"""
        height = 180
        panel_rect = pygame.Rect(x, y, width, height)
        self.draw_rounded_rect(self.screen, UI_PANEL, panel_rect, CORNER_RADIUS)
        self.draw_rounded_rect(self.screen, UI_ACCENT, panel_rect, CORNER_RADIUS, 2)
        
        # Controls title
        title_text = "Controls"
        title_surface = self.subtitle_font.render(title_text, True, UI_TEXT)
        self.screen.blit(title_surface, (x + PANEL_PADDING, y + PANEL_PADDING))
        
        # Instructions
        instructions = [
            "🎮 Click piece to select",
            "📍 Click destination to move",
            "🔄 R - Reset Game",
            "❌ ESC - Quit",
            "💡 Valid moves shown in green"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.body_font.render(instruction, True, UI_TEXT)
            self.screen.blit(text_surface, (x + PANEL_PADDING, y + 50 + i * 25))
    
    def draw_rounded_rect(self, surface, color, rect, radius, width=0):
        """Draw a rounded rectangle"""
        if width == 0:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
        else:
            pygame.draw.rect(surface, color, rect, width, border_radius=radius)
    
    def draw_coordinates(self):
        """Draw elegant file and rank labels"""
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        # Files (a-h) with background
        for col in range(8):
            letter = chr(ord('a') + col)
            text_surface = self.body_font.render(letter, True, UI_TEXT)
            x = board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2 - text_surface.get_width() // 2
            y = board_y + BOARD_HEIGHT + 8
            
            # Background circle for better visibility
            bg_rect = pygame.Rect(x - 8, y - 2, 16, 16)
            self.draw_rounded_rect(self.screen, UI_PANEL, bg_rect, 8)
            self.screen.blit(text_surface, (x, y))
        
        # Ranks (1-8) with background
        for row in range(8):
            number = str(8 - row)
            text_surface = self.body_font.render(number, True, UI_TEXT)
            x = board_x - 25
            y = board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2 - text_surface.get_height() // 2
            
            # Background circle for better visibility
            bg_rect = pygame.Rect(x - 2, y - 2, 16, 16)
            self.draw_rounded_rect(self.screen, UI_PANEL, bg_rect, 8)
            self.screen.blit(text_surface, (x, y))
    
    def render(self, board):
        """Main render method with animation support"""
        self.animation_time += self.clock.get_time() / 1000.0
        
        # Draw gradient background
        self.draw_gradient_background()
        
        # Draw board
        self.draw_board(board)
        
        # Draw pieces
        self.draw_pieces(board)
        
        # Draw UI
        self.draw_ui(board)
        
        # Update display
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS for smooth animations