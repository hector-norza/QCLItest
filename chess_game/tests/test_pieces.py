import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from board import Board
from constants import WHITE_PIECE, BLACK_PIECE

class TestPieces(unittest.TestCase):
    def setUp(self):
        """Set up test board before each test"""
        self.board = Board()
    
    def test_pawn_initial_moves(self):
        """Test pawn can move 1 or 2 squares initially"""
        pawn = self.board.get_piece_at(6, 4)  # White pawn
        moves = pawn.get_valid_moves(self.board)
        
        # Should be able to move 1 or 2 squares forward
        self.assertIn((5, 4), moves)
        self.assertIn((4, 4), moves)
        self.assertEqual(len(moves), 2)
    
    def test_pawn_single_move_after_first(self):
        """Test pawn can only move 1 square after first move"""
        # Move pawn first
        self.board.move_piece((6, 4), (5, 4))
        pawn = self.board.get_piece_at(5, 4)
        moves = pawn.get_valid_moves(self.board)
        
        # Should only be able to move 1 square
        self.assertIn((4, 4), moves)
        self.assertNotIn((3, 4), moves)
        self.assertEqual(len(moves), 1)
    
    def test_rook_moves(self):
        """Test rook moves horizontally and vertically"""
        # Clear path for rook
        self.board.set_piece_at(7, 1, None)  # Remove knight
        self.board.set_piece_at(6, 0, None)  # Remove pawn
        
        rook = self.board.get_piece_at(7, 0)
        moves = rook.get_valid_moves(self.board)
        
        # Should be able to move up the file and along the rank
        self.assertIn((6, 0), moves)
        self.assertIn((5, 0), moves)
        self.assertIn((7, 1), moves)
    
    def test_knight_moves(self):
        """Test knight L-shaped moves"""
        knight = self.board.get_piece_at(7, 1)
        moves = knight.get_valid_moves(self.board)
        
        # Knight should have 2 valid moves from starting position
        self.assertIn((5, 0), moves)
        self.assertIn((5, 2), moves)
        self.assertEqual(len(moves), 2)
    
    def test_king_moves(self):
        """Test king one-square moves"""
        # Clear space around king
        self.board.set_piece_at(6, 3, None)
        self.board.set_piece_at(6, 4, None)
        self.board.set_piece_at(6, 5, None)
        
        king = self.board.get_piece_at(7, 4)
        moves = king.get_valid_moves(self.board)
        
        # King should be able to move to adjacent squares
        self.assertIn((6, 4), moves)
        self.assertTrue(len(moves) > 0)

if __name__ == '__main__':
    unittest.main()