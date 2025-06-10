#!/usr/bin/env python3
"""
Unicode vs ASCII Chess Pieces Comparison Demo
Shows the difference between Unicode symbols and ASCII letters
"""

import pygame
import sys
import os
sys.path.append('src')

from src.constants import *
from src.board import Board
from src.ui.renderer import Renderer

def demo_symbol_comparison():
    """Demo both Unicode and ASCII symbols side by side"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Symbols Comparison - SPACE to toggle")
    
    # Create game objects
    board = Board()
    renderer = Renderer(screen)
    
    clock = pygame.time.Clock()
    running = True
    use_unicode = not USE_ASCII_PIECES  # Start with current setting
    
    print("🎮 Chess Symbols Comparison Demo")
    print("=" * 50)
    print("Current setting:", "Unicode" if not USE_ASCII_PIECES else "ASCII")
    print("Unicode support detected:", renderer.unicode_supported)
    if renderer.unicode_font_name:
        print("Unicode font:", renderer.unicode_font_name)
    print("\nControls:")
    print("SPACE - Toggle between Unicode and ASCII")
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
                    # Toggle between Unicode and ASCII
                    use_unicode = not use_unicode
                    # Temporarily override the setting
                    import src.constants as const
                    const.USE_ASCII_PIECES = not use_unicode
                    
                    # Recreate renderer to apply new setting
                    renderer = Renderer(screen)
                    
                    mode = "Unicode Symbols" if use_unicode else "ASCII Letters"
                    print(f"🔄 Switched to: {mode}")
        
        # Render the game
        renderer.render(board)
        
        # Show current mode
        font = pygame.font.SysFont('Arial', 24, bold=True)
        mode_text = "Unicode Symbols (♔♕♖♗♘♙)" if use_unicode else "ASCII Letters (KQRBNP)"
        text_surface = font.render(f"Mode: {mode_text}", True, (50, 50, 50))
        screen.blit(text_surface, (10, WINDOW_HEIGHT - 35))
        
        # Instructions
        inst_surface = font.render("SPACE = Toggle Mode, ESC = Exit", True, (100, 100, 100))
        screen.blit(inst_surface, (10, WINDOW_HEIGHT - 60))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    demo_symbol_comparison()
