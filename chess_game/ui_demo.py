#!/usr/bin/env python3
"""
UI Enhancement Demo - Chess Game
This script demonstrates the enhanced UI features of the chess game.
"""

import pygame
import sys
import os
sys.path.append('src')

from src.constants import *
from src.board import Board
from src.ui.renderer import Renderer

def demo_ui_enhancements():
    """Demonstrate the beautiful UI enhancements"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Game - Enhanced UI Demo")
    
    # Create game objects
    board = Board()
    renderer = Renderer(screen)
    
    # Make a few moves to show the game in action
    board.select_piece(6, 4)  # Select white pawn e2
    board.make_move(4, 4)     # Move to e4
    board.select_piece(1, 4)  # Select black pawn e7
    board.make_move(3, 4)     # Move to e5
    board.select_piece(7, 1)  # Select white knight b1
    board.make_move(5, 2)     # Move to c3
    
    clock = pygame.time.Clock()
    running = True
    show_info = True
    demo_mode = 0  # 0 = outline pieces, 1 = background circles
    
    print("🎮 Chess Game UI Enhancement Demo")
    print("=" * 50)
    print("Features demonstrated:")
    print("✨ Gradient background")
    print("🎨 Modern color palette")
    print("🔵 Rounded UI panels")
    print("💫 Animated highlights and selection")
    print("🎯 Enhanced piece rendering")
    print("📍 Beautiful coordinate labels")
    print("🎪 Smooth animations at 60 FPS")
    print("🎨 Two piece rendering modes")
    print("\nControls:")
    print("SPACE - Toggle piece rendering mode")
    print("I - Toggle info display")
    print("ESC - Exit demo")
    print("=" * 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Toggle between rendering modes
                    demo_mode = 1 - demo_mode
                    # Update the global constant
                    import src.constants as const
                    const.USE_BACKGROUND_CIRCLES = bool(demo_mode)
                    print(f"🎨 Switched to {'Background Circles' if demo_mode else 'Outline'} rendering mode")
                elif event.key == pygame.K_i:
                    show_info = not show_info
                    print(f"ℹ️  Info display: {'ON' if show_info else 'OFF'}")
        
        # Render the enhanced UI
        renderer.render(board)
        
        # Show current rendering mode
        if show_info:
            mode_text = "Background Circles" if demo_mode else "Outline Pieces"
            font = pygame.font.Font(None, 24)
            text_surface = font.render(f"Mode: {mode_text} (SPACE to toggle)", True, UI_ACCENT)
            screen.blit(text_surface, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    demo_ui_enhancements()
