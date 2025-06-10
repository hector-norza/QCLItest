from abc import ABC, abstractmethod
import pygame

class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.image = None
    
    @abstractmethod
    def get_valid_moves(self, board):
        """Return list of valid moves for this piece"""
        pass
    
    @abstractmethod
    def get_piece_type(self):
        """Return the piece type as string"""
        pass
    
    def move_to(self, new_position):
        """Move piece to new position"""
        self.position = new_position
        self.has_moved = True
    
    def is_white(self):
        return self.color == 'white'
    
    def is_black(self):
        return self.color == 'black'
    
    def copy(self):
        """Create a copy of this piece"""
        piece_copy = self.__class__(self.color, self.position)
        piece_copy.has_moved = self.has_moved
        return piece_copy
    
    def __str__(self):
        return f"{self.color} {self.get_piece_type()} at {self.position}"