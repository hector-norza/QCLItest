from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return KING
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # King can move one square in any direction
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or target_piece.color != self.color:
                    # TODO: Add check validation (king can't move into check)
                    moves.append((new_row, new_col))
        
        # TODO: Add castling logic
        
        return moves