#!/usr/bin/env python3
"""
ASCII vs Unicode Chess Pieces Demo
This script demonstrates the difference between ASCII and Unicode chess piece symbols.
"""

import pygame
import sys
import os
sys.path.append('src')

from src.constants import *
from src.board import Board
from src.ui.renderer import Renderer

def toggle_piece_mode():
    """Toggle between ASCII and Unicode piece symbols"""
    global current_ascii_mode
    current_ascii_mode = not current_ascii_mode
    # Update the global constant dynamically
    import src.constants as const
    const.USE_ASCII_PIECES = current_ascii_mode
    return current_ascii_mode

def demo_piece_symbols():
    """Demonstrate ASCII vs Unicode chess piece symbols"""
    global current_ascii_mode
    current_ascii_mode = True  # Start with ASCII
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Pieces Demo - ASCII vs Unicode")
    
    # Create game objects
    board = Board()
    renderer = Renderer(screen)
    
    # Make a few moves to show different pieces
    board.select_piece(6, 4)  # Select white pawn e2
    board.make_move(4, 4)     # Move to e4
    board.select_piece(1, 3)  # Select black pawn d7
    board.make_move(3, 3)     # Move to d5
    
    clock = pygame.time.Clock()
    running = True
    
    print("🎮 Chess Pieces Symbol Demo")
    print("=" * 40)
    print("Compare ASCII vs Unicode chess piece symbols!")
    print("")
    print("ASCII Mode (default):")
    print("  White: K Q R B N P")
    print("  Black: k q r b n p")
    print("")
    print("Unicode Mode:")
    print("  White: ♔ ♕ ♖ ♗ ♘ ♙")
    print("  Black: ♚ ♛ ♜ ♝ ♞ ♟")
    print("")
    print("Controls:")
    print("SPACE - Toggle between ASCII/Unicode")
    print("R - Reset board")
    print("ESC - Exit demo")
    print("=" * 40)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    mode = toggle_piece_mode()
                    mode_str = "ASCII" if mode else "Unicode"
                    print(f"🔄 Switched to {mode_str} piece symbols")
                elif event.key == pygame.K_r:
                    board = Board()
                    print("🔄 Board reset")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Simple click handling for demo
                    board_x = mouse_pos[0] - UI_MARGIN
                    board_y = mouse_pos[1] - UI_MARGIN
                    
                    if (0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT):
                        col = board_x // SQUARE_SIZE
                        row = board_y // SQUARE_SIZE
                        
                        if 0 <= row < 8 and 0 <= col < 8:
                            if board.selected_piece:
                                board.make_move(row, col)
                            else:
                                board.select_piece(row, col)
        
        # Render the game
        renderer.render(board)
        
        # Show current mode
        font = pygame.font.Font(None, 24)
        mode_text = "ASCII Mode" if current_ascii_mode else "Unicode Mode"
        text_surface = font.render(f"Current: {mode_text} (SPACE to toggle)", True, UI_ACCENT)
        screen.blit(text_surface, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    demo_piece_symbols()
