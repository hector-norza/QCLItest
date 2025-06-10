#!/usr/bin/env python3
"""
Unicode Chess Symbol Test - Visual verification
"""

import pygame
import sys
import os
sys.path.append('src')
from src.constants import *

def test_unicode_rendering():
    pygame.init()
    
    # Create a larger window to see the symbols clearly
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Unicode Chess Symbol Test")
    
    # Test different fonts
    fonts_to_test = [
        ('DejaVu Sans', pygame.font.SysFont('DejaVu Sans', 48)),
        ('Arial Unicode MS', pygame.font.SysFont('Arial Unicode MS', 48)),
        ('Lucida Grande', pygame.font.SysFont('Lucida Grande', 48)),
        ('Times New Roman', pygame.font.SysFont('Times New Roman', 48)),
        ('Default Font', pygame.font.Font(None, 48)),
    ]
    
    # Chess symbols to test
    chess_symbols = ['♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟']
    
    clock = pygame.time.Clock()
    running = True
    
    print("🎮 Unicode Chess Symbol Visual Test")
    print("=" * 50)
    print("If you see squares instead of chess pieces, the font doesn't support Unicode")
    print("ESC - Exit test")
    print("=" * 50)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill((240, 240, 240))
        
        # Title
        title_font = pygame.font.Font(None, 36)
        title = title_font.render("Unicode Chess Symbol Test", True, (0, 0, 0))
        screen.blit(title, (50, 20))
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst1 = inst_font.render("If you see chess pieces below, Unicode works!", True, (0, 0, 0))
        inst2 = inst_font.render("If you see squares/rectangles, Unicode doesn't work.", True, (0, 0, 0))
        screen.blit(inst1, (50, 60))
        screen.blit(inst2, (50, 80))
        
        y_offset = 120
        
        # Test each font
        for font_name, font in fonts_to_test:
            if font is None:
                continue
                
            # Font name
            name_surface = inst_font.render(f"{font_name}:", True, (0, 0, 0))
            screen.blit(name_surface, (50, y_offset))
            
            # Render chess symbols
            x_offset = 200
            for symbol in chess_symbols:
                try:
                    symbol_surface = font.render(symbol, True, (0, 0, 0))
                    screen.blit(symbol_surface, (x_offset, y_offset))
                    x_offset += 50
                except:
                    # If rendering fails, show 'X'
                    error_surface = font.render('X', True, (255, 0, 0))
                    screen.blit(error_surface, (x_offset, y_offset))
                    x_offset += 50
            
            y_offset += 60
        
        # ASCII fallback comparison
        ascii_font = pygame.font.SysFont('Arial', 48, bold=True)
        ascii_label = inst_font.render("ASCII Fallback:", True, (0, 0, 0))
        screen.blit(ascii_label, (50, y_offset))
        
        ascii_symbols = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
        x_offset = 200
        for symbol in ascii_symbols:
            symbol_surface = ascii_font.render(symbol, True, (0, 0, 0))
            screen.blit(symbol_surface, (x_offset, y_offset))
            x_offset += 50
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_unicode_rendering()
