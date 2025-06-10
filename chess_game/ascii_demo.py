#!/usr/bin/env python3
"""
ASCII Chess Pieces Demo - Shows clear letter-based pieces
"""

import pygame
import sys
import os
sys.path.append('src')

from src.constants import *
from src.board import Board
from src.ui.renderer import Renderer

def show_piece_symbols():
    """Demo the ASCII chess piece symbols"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Game - ASCII Pieces Demo")
    
    # Create game objects
    board = Board()
    renderer = Renderer(screen)
    
    clock = pygame.time.Clock()
    running = True
    
    print("🎮 ASCII Chess Pieces Demo")
    print("=" * 40)
    print("Current pieces on the board:")
    print("White pieces: K Q R B N P (uppercase)")
    print("Black pieces: k q r b n p (lowercase)")
    print("")
    print("Board layout:")
    print("  a b c d e f g h")
    for row in range(8):
        line = f"{8-row} "
        for col in range(8):
            piece = board.get_piece_at(row, col)
            if piece:
                symbol = renderer.get_piece_symbol(piece)
                line += f"{symbol} "
            else:
                line += ". "
        print(line)
    print("")
    print("Controls:")
    print("ESC - Exit demo")
    print("Click pieces to select and move them!")
    print("=" * 40)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Simple click handling for demo
                    board_x = mouse_pos[0] - UI_MARGIN
                    board_y = mouse_pos[1] - UI_MARGIN
                    if 0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT:
                        col = board_x // SQUARE_SIZE
                        row = board_y // SQUARE_SIZE
                        if 0 <= row < 8 and 0 <= col < 8:
                            piece = board.get_piece_at(row, col)
                            if piece:
                                symbol = renderer.get_piece_symbol(piece)
                                piece_name = piece.get_piece_type().capitalize()
                                color = "White" if piece.is_white() else "Black"
                                print(f"Clicked: {color} {piece_name} ('{symbol}') at {chr(ord('a')+col)}{8-row}")
        
        # Render the game
        renderer.render(board)
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    show_piece_symbols()
