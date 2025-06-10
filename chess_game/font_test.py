#!/usr/bin/env python3
"""
Unicode Chess Symbol Test - Comprehensive font testing for macOS
This script tests various fonts to find the best one for Unicode chess symbols.
"""

import pygame
import sys
import os
sys.path.append('src')

def test_unicode_fonts():
    """Test various fonts for Unicode chess symbol support"""
    pygame.init()
    
    # Chess symbols to test
    test_symbols = ['♔', '♕', '♖', '♗', '♘', '♙', '♚', '♛', '♜', '♝', '♞', '♟']
    
    # Comprehensive list of macOS fonts that support Unicode
    fonts_to_test = [
        # Apple system fonts with excellent Unicode support
        'Apple Symbols',
        'Apple Color Emoji', 
        'SF Pro Display',
        'SF Pro Text',
        'Helvetica Neue',
        'Arial Unicode MS',
        'Lucida Grande',
        'Menlo',
        'Monaco',
        
        # Common Unicode fonts
        'DejaVu Sans',
        'DejaVu Serif', 
        'Noto Sans',
        'Noto Serif',
        'FreeSans',
        'FreeSerif',
        
        # Standard fallbacks
        'Arial',
        'Helvetica',
        'Times New Roman',
        'Courier New',
    ]
    
    print("🔍 Testing Unicode Chess Symbol Support on macOS")
    print("=" * 60)
    
    working_fonts = []
    
    for font_name in fonts_to_test:
        try:
            # Try to load the font
            test_font = pygame.font.SysFont(font_name, 24, bold=True)
            if test_font is None:
                continue
                
            # Test rendering each chess symbol
            symbols_working = 0
            total_symbols = len(test_symbols)
            
            for symbol in test_symbols:
                try:
                    surface = test_font.render(symbol, True, (255, 255, 255))
                    # Check if symbol rendered with reasonable width
                    if surface.get_width() > 8:  # Minimum width for proper rendering
                        symbols_working += 1
                except:
                    pass
            
            # Calculate success rate
            success_rate = (symbols_working / total_symbols) * 100
            
            if success_rate >= 90:  # 90% or more symbols working
                status = "✅ EXCELLENT"
                working_fonts.append((font_name, success_rate, "excellent"))
            elif success_rate >= 70:  # 70-89% symbols working
                status = "🟡 GOOD"
                working_fonts.append((font_name, success_rate, "good"))
            elif success_rate >= 50:  # 50-69% symbols working
                status = "🟠 PARTIAL"
                working_fonts.append((font_name, success_rate, "partial"))
            else:
                status = "❌ POOR"
            
            print(f"{font_name:20} | {symbols_working:2}/{total_symbols} symbols | {success_rate:5.1f}% | {status}")
            
        except Exception as e:
            print(f"{font_name:20} | Font not available")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if working_fonts:
        # Sort by success rate
        working_fonts.sort(key=lambda x: x[1], reverse=True)
        
        print("🏆 Best fonts for Unicode chess symbols:")
        for i, (font_name, rate, quality) in enumerate(working_fonts[:5]):
            print(f"{i+1}. {font_name} ({rate:.1f}% success)")
        
        # Get the best font
        best_font = working_fonts[0]
        print(f"\n🎯 RECOMMENDED: {best_font[0]} ({best_font[1]:.1f}% success)")
        
        return best_font[0]
    else:
        print("❌ No fonts found with good Unicode chess symbol support")
        print("💡 Recommendation: Install DejaVu fonts using Homebrew:")
        print("   brew install font-dejavu")
        return None

def test_chess_symbols_rendering(font_name):
    """Test rendering of all chess symbols with the specified font"""
    print(f"\n🎨 Testing chess symbol rendering with {font_name}")
    print("-" * 50)
    
    try:
        font = pygame.font.SysFont(font_name, 32, bold=True)
        
        symbols = {
            'White King': '♔',
            'White Queen': '♕', 
            'White Rook': '♖',
            'White Bishop': '♗',
            'White Knight': '♘',
            'White Pawn': '♙',
            'Black King': '♚',
            'Black Queen': '♛',
            'Black Rook': '♜', 
            'Black Bishop': '♝',
            'Black Knight': '♞',
            'Black Pawn': '♟',
        }
        
        print("Chess piece symbols:")
        for piece_name, symbol in symbols.items():
            try:
                surface = font.render(symbol, True, (255, 255, 255))
                width = surface.get_width()
                height = surface.get_height()
                status = "✅" if width > 10 else "❌"
                print(f"{piece_name:12} | {symbol} | {width:3}×{height:2}px | {status}")
            except Exception as e:
                print(f"{piece_name:12} | {symbol} | ERROR: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing font {font_name}: {e}")
        return False

if __name__ == "__main__":
    print("🎮 Unicode Chess Symbols Font Test for macOS")
    print("This will help find the best font for your chess game.\n")
    
    # Test fonts
    best_font = test_unicode_fonts()
    
    if best_font:
        # Test the best font in detail
        test_chess_symbols_rendering(best_font)
        
        print(f"\n🔧 TO USE THIS FONT IN YOUR CHESS GAME:")
        print(f"Edit src/constants.py and set:")
        print(f"PREFERRED_UNICODE_FONT = '{best_font}'")
        print(f"USE_ASCII_PIECES = False")
        
    pygame.quit()
    print("\n✅ Font testing complete!")
