#!/usr/bin/env python3
"""
Simple test script to verify chess game components work
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from board import Board
from pieces import Pawn, King, Queen
from constants import WHITE_PIECE, BLACK_PIECE

def test_basic_functionality():
    print("Testing chess game components...")
    
    # Test board creation
    board = Board()
    print("✓ Board created successfully")
    
    # Test initial piece placement
    white_pawn = board.get_piece_at(6, 0)
    assert isinstance(white_pawn, Pawn), "Expected pawn at (6,0)"
    assert white_pawn.color == WHITE_PIECE, "Expected white pawn"
    print("✓ Initial piece placement correct")
    
    # Test piece movement
    board.select_piece(6, 4)  # Select white pawn
    valid_moves = board.valid_moves
    assert len(valid_moves) > 0, "Pawn should have valid moves"
    print("✓ Piece selection and move validation working")
    
    # Test making a move
    success = board.make_move(4, 4)  # Move pawn forward 2 squares
    assert success, "Move should be successful"
    assert board.current_player == BLACK_PIECE, "Turn should switch to black"
    print("✓ Move execution and turn switching working")
    
    print("\nAll basic tests passed! 🎉")
    print("Your chess game is ready to play!")
    print("\nTo run the game:")
    print("cd chess_game/src && python3 main.py")
    print("\nControls:")
    print("- Click on a piece to select it")
    print("- Click on a highlighted square to move")
    print("- Press R to reset the game")
    print("- Press ESC to quit")

if __name__ == "__main__":
    test_basic_functionality()
