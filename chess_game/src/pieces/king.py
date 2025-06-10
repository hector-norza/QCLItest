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
                    # For now, skip the check validation to avoid recursion
                    moves.append((new_row, new_col))
        
        # Check for castling - simplified for now
        if not self.has_moved:
            # Kingside castling - basic check
            if self._can_castle_simple(board, row, col, 7):
                moves.append((row, col + 2))
            
            # Queenside castling - basic check
            if self._can_castle_simple(board, row, col, 0):
                moves.append((row, col - 2))
        
        return moves
        
    def _can_castle_simple(self, board, row, col, rook_col):
        """Simplified castling check to avoid recursion"""
        # Check if rook is in place and hasn't moved
        rook = board.get_piece_at(row, rook_col)
        if not rook or rook.get_piece_type() != ROOK or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        start = min(col, rook_col) + 1
        end = max(col, rook_col)
        for c in range(start, end):
            if board.get_piece_at(row, c):
                return False
                
        return True
        
    def _can_castle_kingside(self, board):
        """Check if kingside castling is possible"""
        row, col = self.position
        
        # Check if king is in check
        if board.is_in_check(self.color):
            return False
        
        # Check if rook is in place and hasn't moved
        rook_col = 7
        rook = board.get_piece_at(row, rook_col)
        if not rook or rook.get_piece_type() != ROOK or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(col + 1, rook_col):
            if board.get_piece_at(row, c):
                return False
        
        # Check if king passes through check
        for c in range(col + 1, col + 3):
            temp_board = self._simulate_move(board, (row, col), (row, c))
            if temp_board.is_in_check(self.color):
                return False
        
        return True

    def _can_castle_queenside(self, board):
        """Check if queenside castling is possible"""
        row, col = self.position
        
        # Check if king is in check
        if board.is_in_check(self.color):
            return False
        
        # Check if rook is in place and hasn't moved
        rook_col = 0
        rook = board.get_piece_at(row, rook_col)
        if not rook or rook.get_piece_type() != ROOK or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for c in range(rook_col + 1, col):
            if board.get_piece_at(row, c):
                return False
        
        # Check if king passes through check
        for c in range(col - 1, col - 3, -1):
            temp_board = self._simulate_move(board, (row, col), (row, c))
            if temp_board.is_in_check(self.color):
                return False
        
        return True

    def _simulate_move(self, board, from_pos, to_pos):
        """Simulate a move to check for check"""
        # Create a copy of the board
        import copy
        temp_board = copy.deepcopy(board)
        
        # Make the move on the copy
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = temp_board.get_piece_at(from_row, from_col)
        
        if piece:
            temp_board.set_piece_at(to_row, to_col, piece)
            temp_board.set_piece_at(from_row, from_col, None)
            piece.position = (to_row, to_col)
        
        return temp_board