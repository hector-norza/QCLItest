import pygame
from constants import *
from pieces import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = WHITE_PIECE
        self.selected_piece = None
        self.selected_position = None
        self.valid_moves = []
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
        if piece:
            self.set_piece_at(to_row, to_col, piece)
            self.set_piece_at(from_row, from_col, None)
            piece.move_to((to_row, to_col))
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
            self.move_piece(self.selected_position, (to_row, to_col))
            self.clear_selection()
            return True
        return False