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
        self.unicode_font_name = None
        self.unicode_supported = False
        self.game = None  # Reference to the game object
        
        # Test and load the best Unicode font
        self.unicode_font_name = self._find_best_unicode_font()
        
        # Load fonts based on Unicode support
        if self.unicode_font_name and not USE_ASCII_PIECES:
            self._load_unicode_fonts()
            print(f"✅ Using Unicode chess symbols with font: {self.unicode_font_name}")
        else:
            self._load_fallback_fonts()
            print("ℹ️  Using ASCII letters for chess pieces")
        
        # Define piece symbols
        self._setup_piece_symbols()
        
        # Create surfaces for smooth rendering
        self.board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.ui_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def _find_best_unicode_font(self):
        """Find the best font for Unicode chess symbols"""
        if USE_ASCII_PIECES:
            return None
            
        test_symbol = '♔'  # White king symbol
        
        for font_name in PREFERRED_UNICODE_FONTS:
            try:
                # Try to load the font
                test_font = pygame.font.SysFont(font_name, 24, bold=True)
                if test_font is None:
                    continue
                
                # Test if it can render chess symbols
                test_surface = test_font.render(test_symbol, True, (255, 255, 255))
                
                # Check if it rendered properly (width > 8 pixels means it's not just a tiny fallback)
                if test_surface.get_width() > 8:
                    self.unicode_supported = True
                    return font_name
                    
            except Exception:
                continue
        
        return None
    
    def _load_unicode_fonts(self):
        """Load fonts optimized for Unicode chess symbols"""
        try:
            self.title_font = pygame.font.SysFont(self.unicode_font_name, TITLE_FONT_SIZE, bold=True)
            self.subtitle_font = pygame.font.SysFont(self.unicode_font_name, SUBTITLE_FONT_SIZE, bold=True)
            self.body_font = pygame.font.SysFont(self.unicode_font_name, BODY_FONT_SIZE)
            self.small_font = pygame.font.SysFont(self.unicode_font_name, SMALL_FONT_SIZE)
            self.piece_font = pygame.font.SysFont(self.unicode_font_name, int(SQUARE_SIZE * 0.7), bold=True)
        except Exception:
            self._load_fallback_fonts()
    
    def _load_fallback_fonts(self):
        """Load fallback fonts for ASCII mode"""
        try:
            self.title_font = pygame.font.SysFont('Arial', TITLE_FONT_SIZE, bold=True)
            self.subtitle_font = pygame.font.SysFont('Arial', SUBTITLE_FONT_SIZE, bold=True)
            self.body_font = pygame.font.SysFont('Arial', BODY_FONT_SIZE)
            self.small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE)
            self.piece_font = pygame.font.SysFont('Arial', int(SQUARE_SIZE * 0.8), bold=True)
        except Exception:
            # Final fallback to pygame default fonts
            self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
            self.subtitle_font = pygame.font.Font(None, SUBTITLE_FONT_SIZE)
            self.body_font = pygame.font.Font(None, BODY_FONT_SIZE)
            self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
            self.piece_font = pygame.font.Font(None, int(SQUARE_SIZE * 0.8))
    
    def _setup_piece_symbols(self):
        """Setup piece symbols based on Unicode support"""
        # Unicode chess symbols (what we want to use)
        self.unicode_symbols = {
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
        
        # ASCII fallback symbols
        self.ascii_symbols = {
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
    
    def get_piece_symbol(self, piece):
        """Get the appropriate piece symbol based on font support"""
        # If we have Unicode support and it's enabled, use Unicode symbols
        if not USE_ASCII_PIECES and self.unicode_supported:
            return self.unicode_symbols.get((piece.color, piece.get_piece_type()), '?')
        else:
            # Use ASCII letters as fallback
            return self.ascii_symbols.get((piece.color, piece.get_piece_type()), '?')
    
    def draw_gradient_background(self):
        """Draw clean gradient background without animations"""
        # Use fixed colors for a clean, static gradient
        start_color = GRADIENT_START
        end_color = GRADIENT_END
        
        # Simple top-to-bottom gradient
        for y in range(WINDOW_HEIGHT):
            # Calculate color based on position
            ratio = y / WINDOW_HEIGHT
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            
            # Draw horizontal line with calculated color
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def draw_board(self, board):
        """Draw the chess board with clean, modern styling without animations"""
        # Calculate board position
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        # Draw simple shadow
        shadow_rect = pygame.Rect(
            board_x + 5, 
            board_y + 5, 
            BOARD_WIDTH, 
            BOARD_HEIGHT
        )
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=CORNER_RADIUS)
        
        # Draw board background (slightly larger than the squares)
        bg_rect = pygame.Rect(board_x - 3, board_y - 3, BOARD_WIDTH + 6, BOARD_HEIGHT + 6)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=CORNER_RADIUS)
        
        # Draw modern border
        border_rect = pygame.Rect(board_x - 3, board_y - 3, BOARD_WIDTH + 6, BOARD_HEIGHT + 6)
        pygame.draw.rect(self.screen, BOARD_BORDER, border_rect, 3, border_radius=CORNER_RADIUS)
        
        # Draw the actual squares with clean styling
        for row in range(8):
            for col in range(8):
                # Determine square color (no animation)
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                
                # Calculate square position
                x = board_x + col * SQUARE_SIZE
                y = board_y + row * SQUARE_SIZE
                
                # Draw square
                square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, square_rect)
                
                # Add subtle inner shadow for depth (static)
                shadow_alpha = 30
                inner_shadow = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(inner_shadow, (0, 0, 0, shadow_alpha), 
                               (0, 0, SQUARE_SIZE, 10))
                pygame.draw.rect(inner_shadow, (0, 0, 0, shadow_alpha), 
                               (0, 0, 10, SQUARE_SIZE))
                self.screen.blit(inner_shadow, (x, y))
                
                # Highlight selected square (no animation)
                if board.selected_position == (row, col):
                    # Simple highlight
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((*SELECTED_COLOR[:3], 150))
                    self.screen.blit(highlight_surface, (x, y))
                    
                    # Clean border
                    pygame.draw.rect(self.screen, UI_ACCENT, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Highlight valid moves with clean indicators
                if (row, col) in board.valid_moves:
                    center_x = x + SQUARE_SIZE // 2
                    center_y = y + SQUARE_SIZE // 2
                    
                    # Simple circle indicator
                    pygame.draw.circle(self.screen, (*VALID_MOVE_COLOR[:3], 150), (center_x, center_y), 10)
                    pygame.draw.circle(self.screen, UI_SUCCESS, (center_x, center_y), 6)
                    pygame.draw.circle(self.screen, WHITE, (center_x, center_y), 4)
    
    def draw_pieces(self, board):
        """Draw all pieces on the board with clean styling without animations"""
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        # Track the last move for reference
        last_move = board.move_history[-1] if board.move_history else None
        self.last_move = last_move
        
        # Draw pieces in two passes: first non-selected pieces, then selected piece
        # This ensures the selected piece is drawn on top
        
        # First pass: non-selected pieces
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece and board.selected_position != (row, col):
                    # Determine if this piece was just moved
                    just_moved = False
                    if last_move and last_move.to_pos == (row, col):
                        just_moved = True
                    
                    # Use fixed scale without animations
                    scale = PIECE_SCALE
                    
                    # Draw with clean styling
                    if USE_BACKGROUND_CIRCLES:
                        self.draw_piece_with_background(piece, row, col, board_x, board_y, scale, just_moved)
                    else:
                        self.draw_piece(piece, row, col, board_x, board_y, scale, just_moved)
        
        # Second pass: selected piece (drawn on top)
        if board.selected_position:
            row, col = board.selected_position
            piece = board.get_piece_at(row, col)
            if piece:
                # Fixed hover scale without animation
                scale = HOVER_SCALE
                
                # Draw with highlight
                if USE_BACKGROUND_CIRCLES:
                    self.draw_piece_with_background(piece, row, col, board_x, board_y, scale, False, True)
                else:
                    self.draw_piece(piece, row, col, board_x, board_y, scale, False, True)
    
    def draw_piece(self, piece, row, col, board_x=0, board_y=0, scale=1.0, just_moved=False, is_selected=False):
        """Draw a single piece with clean styling without animations"""
        x = board_x + col * SQUARE_SIZE
        y = board_y + row * SQUARE_SIZE
        
        # Use text symbols for pieces
        symbol = self.get_piece_symbol(piece)
        
        # Determine colors with clean styling
        if piece.is_white():
            # Base colors
            text_color = WHITE
            outline_color = BLACK
            
            # Add subtle gold tint to white pieces if selected
            if is_selected:
                text_color = (255, 250, 230)  # Slight gold tint
        else:
            # Base colors
            text_color = BLACK
            outline_color = WHITE
            
            # Add subtle blue tint to black pieces if selected
            if is_selected:
                text_color = (20, 20, 30)  # Slight blue tint
        
        # Scale font for effects
        font_size = int(SQUARE_SIZE * 0.8 * scale)
        if self.unicode_supported and self.unicode_font_name:
            # Use the Unicode-supporting font we found
            try:
                scaled_font = pygame.font.SysFont(self.unicode_font_name, font_size, bold=True)
            except:
                scaled_font = self.piece_font
        else:
            # Use the piece font we loaded
            scaled_font = self.piece_font
        
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2
        
        # Add drop shadow for depth (static)
        shadow_offset = 3
        shadow_surface = scaled_font.render(symbol, True, (0, 0, 0, 100))
        shadow_rect = shadow_surface.get_rect(center=(center_x + shadow_offset, center_y + shadow_offset))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Create outline effect with appropriate thickness
        outline_positions = []
        
        # Standard outline positions
        standard_outline = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        outline_positions.extend(standard_outline)
        
        # Add extra outline for selected pieces
        if is_selected:
            # Add more outline positions for thicker outline
            extra_outline = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            outline_positions.extend(extra_outline)
            
            # Add simple highlight for selected pieces
            glow_color = UI_ACCENT if is_selected else LAST_MOVE_COLOR[:3]
            glow_size = font_size + 4
            
            try:
                glow_font = pygame.font.SysFont(self.unicode_font_name, glow_size, bold=True)
                glow_surface = glow_font.render(symbol, True, (*glow_color, 100))
                glow_rect = glow_surface.get_rect(center=(center_x, center_y))
                self.screen.blit(glow_surface, glow_rect)
            except:
                pass  # Skip glow if font fails
        
        # Draw outline (static, no animation)
        for dx, dy in outline_positions:
            outline_surface = scaled_font.render(symbol, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(center_x + dx, center_y + dy))
            self.screen.blit(outline_surface, outline_rect)
        
        # Draw main piece on top (no animation)
        text_surface = scaled_font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_piece_with_background(self, piece, row, col, board_x=0, board_y=0, scale=1.0, just_moved=False, is_selected=False):
        """Alternative method: Draw piece with clean background styling without animations"""
        x = board_x + col * SQUARE_SIZE
        y = board_y + row * SQUARE_SIZE
        
        # Use text symbols for pieces
        symbol = self.get_piece_symbol(piece)
        
        # Define colors with clean styling
        if piece.is_white():
            # Base colors
            bg_color = WHITE
            text_color = BLACK
            
            # Special styling for selected or just moved pieces
            if is_selected:
                bg_color = (255, 250, 220)  # Warm white
                border_color = UI_ACCENT
            elif just_moved:
                bg_color = (255, 255, 240)  # Slight yellow tint
                border_color = LAST_MOVE_COLOR[:3]
            else:
                border_color = (180, 180, 180)  # Subtle gray border
        else:
            # Base colors
            bg_color = BLACK
            text_color = WHITE
            
            # Special styling for selected or just moved pieces
            if is_selected:
                bg_color = (20, 20, 40)  # Deep blue-black
                border_color = UI_ACCENT
            elif just_moved:
                bg_color = (30, 30, 30)  # Slightly lighter black
                border_color = LAST_MOVE_COLOR[:3]
            else:
                border_color = (80, 80, 80)  # Subtle gray border
        
        # Calculate piece size (static, no animation)
        piece_size = int(SQUARE_SIZE * 0.8 * scale)
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2
        
        # Draw simple shadow
        shadow_offset = 3
        pygame.draw.circle(self.screen, (0, 0, 0, 50), 
                         (center_x + shadow_offset, center_y + shadow_offset), piece_size//2)
        
        # Draw background circle
        pygame.draw.circle(self.screen, bg_color, (center_x, center_y), piece_size//2)
        
        # Draw border with appropriate thickness
        border_width = 2
        if is_selected or just_moved:
            border_width = 3
            
        # Set border color with fixed alpha
        if is_selected:
            border_color = (*UI_ACCENT, 255)
        elif just_moved:
            border_color = (*LAST_MOVE_COLOR[:3], 255)
        else:
            border_color = (*border_color, 200)
            
        pygame.draw.circle(self.screen, border_color, (center_x, center_y), piece_size//2, border_width)
        
        # Scale font for the piece symbol
        font_size = int(SQUARE_SIZE * 0.6 * scale)
        if self.unicode_supported and self.unicode_font_name:
            # Use the Unicode-supporting font we found
            try:
                scaled_font = pygame.font.SysFont(self.unicode_font_name, font_size, bold=True)
            except:
                scaled_font = self.piece_font
        else:
            # Use the piece font we loaded
            scaled_font = self.piece_font
        
        # Draw piece symbol
        text_surface = scaled_font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_ui(self, board):
        """Draw modern game UI elements without animations"""
        # Calculate panel position
        panel_x = BOARD_WIDTH + UI_MARGIN * 2
        panel_y = UI_MARGIN
        panel_width = WINDOW_WIDTH - panel_x - UI_MARGIN
        panel_height = 200
        
        # Draw clean panel with simple gradient
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.draw_rounded_rect(self.screen, UI_PANEL, panel_rect, CORNER_RADIUS)
        
        # Add simple border
        self.draw_rounded_rect(self.screen, UI_ACCENT, panel_rect, CORNER_RADIUS, 2)
        
        # Game title with clean styling
        title_text = "Chess Game"
        title_surface = self.title_font.render(title_text, True, UI_TEXT)
        title_rect = title_surface.get_rect(centerx=panel_x + panel_width // 2, y=panel_y + PANEL_PADDING)
        
        # Add simple shadow for depth
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0, 100))
        shadow_rect = shadow_surface.get_rect(centerx=title_rect.centerx+2, y=title_rect.y+2)
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Current player with clean indicator
        player_y = title_rect.bottom + 20
        player_text = f"Current Player:"
        player_surface = self.subtitle_font.render(player_text, True, UI_TEXT)
        self.screen.blit(player_surface, (panel_x + PANEL_PADDING, player_y))
        
        # Player color indicator (static, no animation)
        indicator_x = panel_x + PANEL_PADDING + player_surface.get_width() + 10
        indicator_color = WHITE if board.current_player == 'white' else BLACK
        border_color = BLACK if board.current_player == 'white' else WHITE
        
        # Simple indicator circle
        indicator_size = 12
        pygame.draw.circle(self.screen, indicator_color, (indicator_x + 15, player_y + 12), indicator_size)
        pygame.draw.circle(self.screen, border_color, (indicator_x + 15, player_y + 12), indicator_size, 2)
        
        # AI status indicator
        if hasattr(self, 'game') and self.game.use_ai:
            ai_text = f"AI: {self.game.ai_player.difficulty.capitalize()}"
            ai_color = UI_ACCENT
            ai_surface = self.body_font.render(ai_text, True, ai_color)
            self.screen.blit(ai_surface, (indicator_x + 40, player_y + 5))
        
        # Game status with clean styling
        status_y = player_y + 35
        if hasattr(board, 'game_status'):
            status_text = board.game_status
            
            # Color based on status (no animation)
            if "wins" in status_text:
                status_color = UI_SUCCESS
            elif "check" in status_text:
                status_color = UI_WARNING
            elif "AI is thinking" in status_text:
                status_color = UI_ACCENT
            else:
                status_color = UI_TEXT
        else:
            status_text = "Game in progress"
            status_color = UI_TEXT
        
        # Render status with simple shadow
        status_shadow = self.body_font.render(status_text, True, (0, 0, 0, 100))
        status_surface = self.body_font.render(status_text, True, status_color)
        self.screen.blit(status_shadow, (panel_x + PANEL_PADDING + 1, status_y + 1))
        self.screen.blit(status_surface, (panel_x + PANEL_PADDING, status_y))
        
        # Draw controls panel
        controls_y = panel_y + panel_height + 20
        self.draw_controls_panel(panel_x, controls_y, panel_width)
        
        # Draw coordinates
        self.draw_coordinates()
    
    def draw_controls_panel(self, x, y, width):
        """Draw the controls panel with clean, modern styling without animations"""
        height = 200  # Increased height for more controls
        
        # Draw clean panel with simple styling
        panel_rect = pygame.Rect(x, y, width, height)
        self.draw_rounded_rect(self.screen, UI_PANEL, panel_rect, CORNER_RADIUS)
        
        # Add simple border
        self.draw_rounded_rect(self.screen, UI_ACCENT, panel_rect, CORNER_RADIUS, 2)
        
        # Controls title with clean styling
        title_text = "Controls"
        title_surface = self.subtitle_font.render(title_text, True, UI_TEXT)
        self.screen.blit(title_surface, (x + PANEL_PADDING, y + PANEL_PADDING))
        
        # Instructions with icons (no animations)
        instructions = [
            ("🎮", "Click piece to select"),
            ("📍", "Click destination to move"),
            ("🔄", "R - Reset Game"),
            ("↩️", "Z - Undo Move"),
            ("🤖", "A - Toggle AI opponent"),
            ("🧠", "D - Cycle AI difficulty"),
            ("❌", "ESC - Quit"),
            ("💡", "Valid moves shown in green")
        ]
        
        for i, (icon, text) in enumerate(instructions):
            # Calculate position
            button_y = y + 50 + i * 25
            
            # Draw icon
            icon_surface = self.body_font.render(icon, True, UI_ACCENT)
            self.screen.blit(icon_surface, (x + PANEL_PADDING, button_y))
            
            # Draw instruction text
            text_surface = self.body_font.render(text, True, UI_TEXT)
            self.screen.blit(text_surface, (x + PANEL_PADDING + 25, button_y))
    
    def draw_rounded_rect(self, surface, color, rect, radius, width=0):
        """Draw a rounded rectangle"""
        if width == 0:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
        else:
            pygame.draw.rect(surface, color, rect, width, border_radius=radius)
    
    def draw_coordinates(self):
        """Draw clean file and rank labels without animations"""
        board_x = UI_MARGIN
        board_y = UI_MARGIN
        
        # Files (a-h) with clean styling
        for col in range(8):
            letter = chr(ord('a') + col)
            
            # Calculate position
            x = board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = board_y + BOARD_HEIGHT + 10
            
            # Draw simple background circle
            bg_size = 20
            pygame.draw.circle(self.screen, UI_PANEL, (x, y), bg_size//2)
            pygame.draw.circle(self.screen, UI_ACCENT, (x, y), bg_size//2, 1)
            
            # Draw text
            text_surface = self.body_font.render(letter, True, UI_TEXT)
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        
        # Ranks (1-8) with clean styling
        for row in range(8):
            number = str(8 - row)
            
            # Calculate position
            x = board_x - 20
            y = board_y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            # Draw simple background circle
            bg_size = 20
            pygame.draw.circle(self.screen, UI_PANEL, (x, y), bg_size//2)
            pygame.draw.circle(self.screen, UI_ACCENT, (x, y), bg_size//2, 1)
            
            # Draw text
            text_surface = self.body_font.render(number, True, UI_TEXT)
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
    
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