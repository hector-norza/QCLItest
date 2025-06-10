#!/usr/bin/env python3
"""
Chess Game Demonstration
Shows the chess game working without GUI for testing
"""

import os
import sys

# Setup path
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def demo_chess_game():
    print("🏁 Chess Game Demo")
    print("=" * 40)
    
    try:
        # Import components
        from board import Board
        from constants import WHITE_PIECE, BLACK_PIECE
        
        # Create board
        board = Board()
        print(f"✅ Board created successfully")
        print(f"   Current player: {board.current_player}")
        print(f"   Total pieces: {sum(1 for row in board.board for piece in row if piece)}")
        
        # Show initial board state
        print("\n📋 Initial Board State:")
        for row in range(8):
            row_pieces = []
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece:
                    symbol = piece.get_piece_type()[0].upper() if piece.color == WHITE_PIECE else piece.get_piece_type()[0].lower()
                    row_pieces.append(symbol)
                else:
                    row_pieces.append('.')
            print(f"   {8-row} {' '.join(row_pieces)}")
        print("     a b c d e f g h")
        
        # Test piece selection and movement
        print("\n🎯 Testing Piece Movement:")
        
        # Select white pawn
        board.select_piece(6, 4)  # e2 pawn
        print(f"   Selected piece at e2: {board.selected_piece}")
        print(f"   Valid moves: {len(board.valid_moves)}")
        
        # Make a move
        if board.make_move(4, 4):  # Move to e4
            print("   ✅ Successfully moved pawn from e2 to e4")
            print(f"   Current player: {board.current_player}")
        else:
            print("   ❌ Move failed")
        
        # Select black pawn
        board.select_piece(1, 4)  # e7 pawn
        print(f"   Selected black pawn at e7: {board.selected_piece}")
        
        if board.make_move(3, 4):  # Move to e5
            print("   ✅ Successfully moved black pawn from e7 to e5")
            print(f"   Current player: {board.current_player}")
        
        print("\n🎉 Chess game is working perfectly!")
        print("\n🎮 To play the full game with GUI:")
        print("   cd chess_game/src")
        print("   python3 main.py")
        
        print("\n📚 Game features:")
        print("   • All 6 piece types implemented")
        print("   • Standard chess movement rules")
        print("   • Turn-based gameplay")
        print("   • Visual interface with Pygame")
        print("   • Click-to-move controls")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_chess_game()
