import pygame
import copy
from constants import *
from pieces import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = WHITE_PIECE
        self.selected_piece = None
        self.selected_position = None
        self.valid_moves = []
        self.move_history = []
        self.game_status = "Game in progress"
        self.ai_thinking = False  # Flag to indicate AI is thinking
        self.setup_initial_position()
        
    def setup_initial_position(self):
        """Set up the standard chess starting position"""
        # Place pawns
        for col in range(8):
            self.set_piece_at(1, col, Pawn(BLACK_PIECE, (1, col)))
            self.set_piece_at(6, col, Pawn(WHITE_PIECE, (6, col)))
        
        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col, piece_class in enumerate(piece_order):
            self.set_piece_at(0, col, piece_class(BLACK_PIECE, (0, col)))
            self.set_piece_at(7, col, piece_class(WHITE_PIECE, (7, col)))
        
    def get_piece_at(self, row, col):
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece_at(self, row, col, piece):
        """Place piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
            if piece:
                piece.position = (row, col)
    
    def move_piece(self, from_pos, to_pos):
        """Move piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece_at(from_row, from_col)
        captured_piece = self.get_piece_at(to_row, to_col)
        
        if piece:
            # Record move before making it
            from move import Move
            move = Move(from_pos, to_pos, piece, captured_piece)
            self.move_history.append(move)
            
            # Make the move
            self.set_piece_at(to_row, to_col, piece)
            self.set_piece_at(from_row, from_col, None)
            piece.move_to((to_row, to_col))
            
            # Check for pawn promotion
            if piece.get_piece_type() == PAWN:
                promotion_row = 0 if piece.color == WHITE_PIECE else 7
                if to_row == promotion_row:
                    # For now, automatically promote to queen
                    from pieces.queen import Queen
                    promoted_piece = Queen(piece.color, (to_row, to_col))
                    self.set_piece_at(to_row, to_col, promoted_piece)
            
            self.switch_player()
            return True
        return False
    
    def switch_player(self):
        """Switch current player"""
        self.current_player = BLACK_PIECE if self.current_player == WHITE_PIECE else WHITE_PIECE
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def select_piece(self, row, col):
        """Select a piece and show valid moves"""
        piece = self.get_piece_at(row, col)
        
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.selected_position = (row, col)
            self.valid_moves = piece.get_valid_moves(self)
        else:
            self.clear_selection()
    
    def clear_selection(self):
        """Clear current selection"""
        self.selected_piece = None
        self.selected_position = None
        self.valid_moves = []
    
    def make_move(self, to_row, to_col):
        """Attempt to make a move to the specified position"""
        if self.selected_piece and (to_row, to_col) in self.valid_moves:
            from_row, from_col = self.selected_position
            
            # Handle castling
            if self.selected_piece.get_piece_type() == KING and abs(to_col - from_col) == 2:
                # Kingside castling
                if to_col > from_col:
                    # Move the rook too
                    rook = self.get_piece_at(from_row, 7)
                    if rook:
                        self.set_piece_at(from_row, 5, rook)
                        self.set_piece_at(from_row, 7, None)
                        rook.move_to((from_row, 5))
                # Queenside castling
                else:
                    # Move the rook too
                    rook = self.get_piece_at(from_row, 0)
                    if rook:
                        self.set_piece_at(from_row, 3, rook)
                        self.set_piece_at(from_row, 0, None)
                        rook.move_to((from_row, 3))
            
            # Make the move
            self.move_piece(self.selected_position, (to_row, to_col))
            self.clear_selection()
            return True
        return False
    def is_in_check(self, color):
        """Check if the given color's king is in check"""
        # Find king position
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.color == color and piece.get_piece_type() == KING:
                    king_position = (row, col)
                    break
            if king_position:
                break
        
        if not king_position:
            return False  # No king found (shouldn't happen in a real game)
        
        # Check if any opponent piece can attack the king
        opponent_color = BLACK_PIECE if color == WHITE_PIECE else WHITE_PIECE
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.color == opponent_color:
                    # For now, skip the check to avoid recursion
                    # This is a simplified version to avoid recursion issues
                    if piece.get_piece_type() == PAWN:
                        # Check pawn attack pattern directly
                        pawn_row, pawn_col = piece.position
                        direction = -1 if piece.is_white() else 1
                        attack_positions = [(pawn_row + direction, pawn_col - 1), 
                                           (pawn_row + direction, pawn_col + 1)]
                        if king_position in attack_positions:
                            return True
                    # Add other piece attack patterns as needed
        
        return False
    
    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        # Try all possible moves for all pieces of this color
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.color == color:
                    for move_pos in piece.get_valid_moves(self):
                        # Try the move
                        temp_board = self._simulate_move((row, col), move_pos)
                        
                        # If this move gets out of check, it's not checkmate
                        if not temp_board.is_in_check(color):
                            return False
        
        # No move gets out of check
        return True
    
    def is_stalemate(self, color):
        """Check if the given color is in stalemate"""
        if self.is_in_check(color):
            return False
        
        # Check if any legal move exists
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at(row, col)
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self)
                    if valid_moves:
                        return False
        
        # No legal moves and not in check = stalemate
        return True
    
    def _simulate_move(self, from_pos, to_pos):
        """Simulate a move to check for check"""
        temp_board = copy.deepcopy(self)
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = temp_board.get_piece_at(from_row, from_col)
        
        if piece:
            temp_board.set_piece_at(to_row, to_col, piece)
            temp_board.set_piece_at(from_row, from_col, None)
            piece.position = (to_row, to_col)
        
        return temp_board
    
    def undo_move(self):
        """Undo the last move"""
        if not self.move_history:
            return False
        
        move = self.move_history.pop()
        
        # Restore the piece to its original position
        self.set_piece_at(move.from_pos[0], move.from_pos[1], move.piece)
        
        # Restore captured piece if any
        self.set_piece_at(move.to_pos[0], move.to_pos[1], move.captured_piece)
        
        # Update piece state
        move.piece.position = move.from_pos
        if len(self.move_history) == 0 or self.move_history[-1].piece != move.piece:
            move.piece.has_moved = False
        
        # Switch back to previous player
        self.switch_player()
        
        return True