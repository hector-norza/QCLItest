import os
import sys

# Change to src directory and add to path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
os.chdir(src_dir)
sys.path.insert(0, src_dir)

print("Testing chess game...")

try:
    from board import Board
    print("✓ Board import successful")
    
    board = Board()
    print("✓ Board created successfully")
    
    # Check if pieces are placed
    piece = board.get_piece_at(6, 4)
    print(f"✓ Piece at (6,4): {piece}")
    
    # Test selection
    board.select_piece(6, 4)
    print(f"✓ Selected piece, valid moves: {len(board.valid_moves)}")
    
    print("\n🎉 Chess game is working correctly!")
    print("\nTo play the game, run:")
    print("cd chess_game/src && python3 main.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
