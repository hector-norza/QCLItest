from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return PAWN
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Direction: white pieces move up (decrease row), black pieces move down (increase row)
        direction = -1 if self.is_white() else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and board.get_piece_at(new_row, col) is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row = row + 2 * direction
                if 0 <= new_row < 8 and board.get_piece_at(new_row, col) is None:
                    moves.append((new_row, col))
        
        # Diagonal captures
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if target_piece and target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves