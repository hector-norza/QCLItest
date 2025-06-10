import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class InputHandler:
    def __init__(self):
        pass
    
    def handle_click(self, mouse_pos, board):
        """Handle mouse click events with UI margin support"""
        x, y = mouse_pos
        
        # Adjust for board offset (UI_MARGIN)
        board_x = x - UI_MARGIN
        board_y = y - UI_MARGIN
        
        # Check if click is within the board bounds
        if (0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT):
            col = board_x // SQUARE_SIZE
            row = board_y // SQUARE_SIZE
            
            # Ensure we're within valid chess board coordinates
            if 0 <= row < 8 and 0 <= col < 8:
                # If a piece is already selected, try to move it
                if board.selected_piece:
                    if board.make_move(row, col):
                        # Move was successful
                        pass
                    else:
                        # Move failed, try selecting new piece
                        board.select_piece(row, col)
                else:
                    # No piece selected, try to select one
                    board.select_piece(row, col)
    
    def get_square_from_mouse(self, mouse_pos):
        """Convert mouse position to board coordinates"""
        x, y = mouse_pos
        if x < BOARD_WIDTH and y < BOARD_HEIGHT:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            return (row, col)
        return None