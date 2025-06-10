from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return ROOK
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target_piece = board.get_piece_at(new_row, new_col)
                
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append((new_row, new_col))
                    break  # Can't move beyond an enemy piece
                else:
                    break  # Can't move beyond a friendly piece
        
        return moves