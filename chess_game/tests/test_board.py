import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from board import Board
from pieces import Pawn, Rook, King
from constants import WHITE_PIECE, BLACK_PIECE

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Set up test board before each test"""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test that board initializes correctly"""
        self.assertEqual(self.board.current_player, WHITE_PIECE)
        self.assertIsNone(self.board.selected_piece)
        self.assertEqual(len(self.board.valid_moves), 0)
    
    def test_initial_piece_placement(self):
        """Test that pieces are placed correctly at start"""
        # Test white pawns
        for col in range(8):
            piece = self.board.get_piece_at(6, col)
            self.assertIsInstance(piece, Pawn)
            self.assertEqual(piece.color, WHITE_PIECE)
        
        # Test black pawns
        for col in range(8):
            piece = self.board.get_piece_at(1, col)
            self.assertIsInstance(piece, Pawn)
            self.assertEqual(piece.color, BLACK_PIECE)
        
        # Test white king
        king = self.board.get_piece_at(7, 4)
        self.assertIsInstance(king, King)
        self.assertEqual(king.color, WHITE_PIECE)
    
    def test_piece_movement(self):
        """Test basic piece movement"""
        # Move white pawn
        self.board.select_piece(6, 4)  # Select white pawn
        self.assertTrue(self.board.make_move(4, 4))  # Move two squares
        
        # Check piece moved
        piece = self.board.get_piece_at(4, 4)
        self.assertIsInstance(piece, Pawn)
        self.assertEqual(piece.color, WHITE_PIECE)
        
        # Check old position is empty
        self.assertIsNone(self.board.get_piece_at(6, 4))
    
    def test_turn_switching(self):
        """Test that turns switch correctly"""
        self.assertEqual(self.board.current_player, WHITE_PIECE)
        
        # Make a move
        self.board.select_piece(6, 4)
        self.board.make_move(4, 4)
        
        # Player should switch
        self.assertEqual(self.board.current_player, BLACK_PIECE)

if __name__ == '__main__':
    unittest.main()