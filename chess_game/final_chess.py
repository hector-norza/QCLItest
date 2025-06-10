#!/usr/bin/env python3
"""
Final Working Chess Game - Clear ASCII Pieces
This version guarantees working piece symbols using ASCII letters.
"""

import pygame
import sys
import os
sys.path.append('src')

from src.constants import *
from src.board import Board
from src.ui.renderer import Renderer
from src.ui.input_handler import InputHandler

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Game - ASCII Pieces")
    
    # Create game objects
    board = Board()
    renderer = Renderer(screen)
    input_handler = InputHandler()
    
    clock = pygame.time.Clock()
    running = True
    
    print("🎮 Chess Game - ASCII Pieces Version")
    print("=" * 40)
    print("White pieces: K Q R B N P (uppercase)")
    print("Black pieces: k q r b n p (lowercase)")
    print("")
    print("Controls:")
    print("• Click piece to select")
    print("• Click destination to move")
    print("• R - Reset game")
    print("• ESC - Quit")
    print("=" * 40)
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    input_handler.handle_click(mouse_pos, board)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = Board()  # Reset game
                    print("🔄 Game reset!")
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Render the game
        renderer.render(board)
        clock.tick(60)
    
    pygame.quit()
    print("👋 Thanks for playing!")

if __name__ == "__main__":
    main()
