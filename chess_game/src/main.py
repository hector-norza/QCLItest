#!/usr/bin/env python3
"""
Chess Game - Main Entry Point
A simple chess game implemented with pygame.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game import Game

def main():
    """Main function to start the chess game"""
    try:
        game = Game()
        game.run()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install pygame: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()