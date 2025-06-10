from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return KNIGHT
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves