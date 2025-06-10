#!/usr/bin/env python3
"""
Visual Demo - Chess Piece Rendering Methods
Shows both outline and background circle rendering methods
"""

import os
import sys
import pygame

# Setup path
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def demo_rendering_methods():
    print("🎨 Chess Piece Rendering Demo")
    print("=" * 40)
    
    try:
        import constants
        from ui.renderer import Renderer
        from board import Board
        
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Chess Piece Rendering Demo")
        clock = pygame.time.Clock()
        
        board = Board()
        
        print("✅ Demo initialized successfully")
        print("\nRendering methods available:")
        print("1. Outline Text (solid white/black with contrasting outlines)")
        print("2. Background Circles (text on contrasting circular backgrounds)")
        
        print(f"\nCurrent method: {'Background Circles' if constants.USE_BACKGROUND_CIRCLES else 'Outline Text'}")
        print("\nClose the demo window to continue...")
        
        # Demo loop
        running = True
        method_switch_time = 0
        current_method = constants.USE_BACKGROUND_CIRCLES
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Toggle rendering method
                        constants.USE_BACKGROUND_CIRCLES = not constants.USE_BACKGROUND_CIRCLES
                        current_method = constants.USE_BACKGROUND_CIRCLES
                        print(f"Switched to: {'Background Circles' if current_method else 'Outline Text'}")
            
            # Clear screen
            screen.fill((240, 240, 240))
            
            # Create two renderers for comparison
            renderer = Renderer(screen)
            
            # Draw title
            font = pygame.font.Font(None, 36)
            method_name = "Background Circles" if constants.USE_BACKGROUND_CIRCLES else "Outline Text"
            title = font.render(f"Method: {method_name} (Press SPACE to toggle)", True, (0, 0, 0))
            screen.blit(title, (10, 10))
            
            # Draw sample pieces
            sample_pieces = [
                (board.get_piece_at(0, 0), 1, 1),  # Black rook
                (board.get_piece_at(0, 4), 1, 2),  # Black king
                (board.get_piece_at(1, 0), 1, 3),  # Black pawn
                (board.get_piece_at(7, 0), 3, 1),  # White rook  
                (board.get_piece_at(7, 4), 3, 2),  # White king
                (board.get_piece_at(6, 0), 3, 3),  # White pawn
            ]
            
            for piece, row, col in sample_pieces:
                if piece:
                    renderer.draw_piece(piece, row, col)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        print("✅ Demo completed successfully")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_rendering_methods()
