#!/usr/bin/env python3
"""
Font Installation Helper for Chess Game Unicode Symbols
This script helps install fonts that support Unicode chess symbols on macOS.
"""

import subprocess
import sys
import os

def check_font_available(font_name):
    """Check if a font is available on the system"""
    try:
        import pygame
        pygame.init()
        font = pygame.font.SysFont(font_name, 24)
        if font:
            # Test rendering a chess symbol
            test_surface = font.render('♔', True, (255, 255, 255))
            return test_surface.get_width() > 10
        return False
    except:
        return False

def install_fonts_macos():
    """Install Unicode-supporting fonts on macOS"""
    print("🎯 Chess Game Font Installation Helper")
    print("=" * 50)
    
    # Check current font availability
    print("Checking available fonts...")
    
    fonts_to_check = [
        'DejaVu Sans',
        'Noto Sans', 
        'Arial Unicode MS',
        'Lucida Grande',
        'SF Pro Display',
        'Segoe UI Symbol',
        'Liberation Sans'
    ]
    
    available_fonts = []
    for font_name in fonts_to_check:
        if check_font_available(font_name):
            available_fonts.append(font_name)
            print(f"✅ {font_name} - Available")
        else:
            print(f"❌ {font_name} - Not available")
    
    if available_fonts:
        print(f"\n🎉 Good news! You have {len(available_fonts)} Unicode-supporting fonts!")
        print("Your chess game should display proper chess symbols.")
        return True
    
    print("\n⚠️  No Unicode fonts found. Let's install some!")
    
    # Install fonts using Homebrew (most common package manager on macOS)
    print("\nInstalling fonts via Homebrew...")
    
    try:
        # Check if Homebrew is installed
        subprocess.run(['brew', '--version'], check=True, capture_output=True)
        print("✅ Homebrew found")
        
        # Install font cask
        print("Installing font-dejavu...")
        result = subprocess.run(['brew', 'install', '--cask', 'font-dejavu'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ DejaVu fonts installed successfully!")
        else:
            print("⚠️  DejaVu installation had issues, but may already be installed")
        
        # Install Noto fonts
        print("Installing font-noto...")
        result = subprocess.run(['brew', 'install', '--cask', 'font-noto'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Noto fonts installed successfully!")
        else:
            print("⚠️  Noto installation had issues, but may already be installed")
            
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Homebrew not found")
        print("\nTo install Homebrew and fonts manually:")
        print("1. Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Install fonts: brew install --cask font-dejavu font-noto")
        print("3. Restart your terminal and run the chess game again")
        return False

def main():
    """Main function"""
    try:
        install_fonts_macos()
        
        print("\n" + "=" * 50)
        print("🎮 Testing Chess Game Fonts")
        print("=" * 50)
        
        # Test the chess game font detection
        sys.path.append('src')
        from src.constants import *
        from src.ui.renderer import Renderer
        import pygame
        
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        renderer = Renderer(screen)
        
        if renderer.unicode_supported:
            print("✅ SUCCESS! Unicode chess symbols are now supported!")
            print(f"Using font: {renderer.piece_font}")
            print("\nYour chess pieces will display as: ♔ ♕ ♖ ♗ ♘ ♙")
        else:
            print("⚠️  Still using ASCII fallback: K Q R B N P")
            print("Try restarting your system and running the game again.")
        
        pygame.quit()
        
        print("\n🚀 Ready to play! Run: python3 src/main.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Falling back to ASCII pieces, which will still work fine!")

if __name__ == "__main__":
    main()
