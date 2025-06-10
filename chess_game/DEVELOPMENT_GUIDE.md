# Chess Game Development Guide: Step-by-Step Tutorial

## Table of Contents
1. [Project Setup](#project-setup)
2. [Constants and Configuration](#constants-and-configuration)
3. [Base Piece Class](#base-piece-class)
4. [Individual Chess Pieces](#individual-chess-pieces)
5. [Game Board](#game-board)
6. [User Interface](#user-interface)
7. [Game Logic](#game-logic)
8. [Testing](#testing)
9. [Running the Game](#running-the-game)

---

## 1. Project Setup

### Step 1.1: Create Project Directory Structure

```bash
# Create the main project directory
mkdir chess_game
cd chess_game

# Create the complete directory structure
mkdir -p assets/images/pieces
mkdir -p assets/sounds
mkdir -p src/pieces
mkdir -p src/ui
mkdir -p tests

# Create all necessary Python files
touch src/__init__.py
touch src/main.py
touch src/constants.py
touch src/board.py
touch src/game.py
touch src/move.py
touch src/pieces/__init__.py
touch src/pieces/piece.py
touch src/pieces/pawn.py
touch src/pieces/rook.py
touch src/pieces/knight.py
touch src/pieces/bishop.py
touch src/pieces/queen.py
touch src/pieces/king.py
touch src/ui/__init__.py
touch src/ui/renderer.py
touch src/ui/input_handler.py
touch tests/__init__.py
touch tests/test_board.py
touch tests/test_pieces.py
touch requirements.txt
touch README.md
```

### Step 1.2: Create Requirements File

Create `requirements.txt`:
```
pygame==2.5.2
```

### Step 1.3: Install Dependencies

```bash
pip3 install -r requirements.txt
```

---

## 2. Constants and Configuration

### Step 2.1: Create Game Constants

Create `src/constants.py`:

```python
import pygame

# Board dimensions
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
BOARD_HEIGHT = BOARD_SIZE * SQUARE_SIZE

# Window dimensions
WINDOW_WIDTH = BOARD_WIDTH + 200  # Extra space for UI
WINDOW_HEIGHT = BOARD_HEIGHT + 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)
VALID_MOVE_COLOR = (0, 255, 0, 128)
RED = (255, 0, 0)

# Piece colors
WHITE_PIECE = 'white'
BLACK_PIECE = 'black'

# Starting positions
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Piece types
PAWN = 'pawn'
ROOK = 'rook'
KNIGHT = 'knight'
BISHOP = 'bishop'
QUEEN = 'queen'
KING = 'king'

# Piece values (for AI evaluation)
PIECE_VALUES = {
    PAWN: 1,
    KNIGHT: 3,
    BISHOP: 3,
    ROOK: 5,
    QUEEN: 9,
    KING: 100
}
```

**Why these constants?**
- `BOARD_SIZE`: Standard chess board is 8x8
- `SQUARE_SIZE`: Pixel size of each square for rendering
- Colors: Standard chess board colors and UI feedback colors
- Piece types: String constants for piece identification
- Piece values: Standard chess piece values for evaluation

---

## 3. Base Piece Class

### Step 3.1: Create Abstract Piece Class

Create `src/pieces/piece.py`:

```python
from abc import ABC, abstractmethod
import pygame

class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.image = None
    
    @abstractmethod
    def get_valid_moves(self, board):
        """Return list of valid moves for this piece"""
        pass
    
    @abstractmethod
    def get_piece_type(self):
        """Return the piece type as string"""
        pass
    
    def move_to(self, new_position):
        """Move piece to new position"""
        self.position = new_position
        self.has_moved = True
    
    def is_white(self):
        return self.color == 'white'
    
    def is_black(self):
        return self.color == 'black'
    
    def copy(self):
        """Create a copy of this piece"""
        piece_copy = self.__class__(self.color, self.position)
        piece_copy.has_moved = self.has_moved
        return piece_copy
    
    def __str__(self):
        return f"{self.color} {self.get_piece_type()} at {self.position}"
```

**Key concepts:**
- **Abstract Base Class**: Ensures all pieces implement required methods
- **Position tracking**: Stores current board position
- **Movement tracking**: `has_moved` flag for castling and pawn rules
- **Color methods**: Helper methods for piece color checking

---

## 4. Individual Chess Pieces

### Step 4.1: Implement Pawn

Create `src/pieces/pawn.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return PAWN
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Direction: white pieces move up (decrease row), black pieces move down (increase row)
        direction = -1 if self.is_white() else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and board.get_piece_at(new_row, col) is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row = row + 2 * direction
                if 0 <= new_row < 8 and board.get_piece_at(new_row, col) is None:
                    moves.append((new_row, col))
        
        # Diagonal captures
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                if target_piece and target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
```

**Pawn movement rules:**
- Forward one square (or two from starting position)
- Captures diagonally
- Cannot move backward

### Step 4.2: Implement Rook

Create `src/pieces/rook.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return ROOK
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target_piece = board.get_piece_at(new_row, new_col)
                
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append((new_row, new_col))
                    break  # Can't move beyond an enemy piece
                else:
                    break  # Can't move beyond a friendly piece
        
        return moves
```

### Step 4.3: Implement Knight

Create `src/pieces/knight.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return KNIGHT
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
```

### Step 4.4: Implement Bishop

Create `src/pieces/bishop.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return BISHOP
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target_piece = board.get_piece_at(new_row, new_col)
                
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append((new_row, new_col))
                    break  # Can't move beyond an enemy piece
                else:
                    break  # Can't move beyond a friendly piece
        
        return moves
```

### Step 4.5: Implement Queen

Create `src/pieces/queen.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return QUEEN
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # Queen moves like both rook and bishop (horizontal, vertical, and diagonal)
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Rook moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Bishop moves
        ]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = row + dr * i
                new_col = col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target_piece = board.get_piece_at(new_row, new_col)
                
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append((new_row, new_col))
                    break  # Can't move beyond an enemy piece
                else:
                    break  # Can't move beyond a friendly piece
        
        return moves
```

### Step 4.6: Implement King

Create `src/pieces/king.py`:

```python
from piece import Piece
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    
    def get_piece_type(self):
        return KING
    
    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        
        # King can move one square in any direction
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or target_piece.color != self.color:
                    # TODO: Add check validation (king can't move into check)
                    moves.append((new_row, new_col))
        
        # TODO: Add castling logic
        
        return moves
```

### Step 4.7: Create Pieces Module

Create `src/pieces/__init__.py`:

```python
import os
import sys

# Add current directory to path so we can import from same directory
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

from piece import Piece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

__all__ = ['Piece', 'Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']
```

---

## 5. Game Board

### Step 5.1: Implement Board Class

Create `src/board.py`:

```python
import pygame
from constants import *
from pieces import *

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = WHITE_PIECE
        self.selected_piece = None
        self.selected_position = None
        self.valid_moves = []
        self.setup_initial_position()
        
    def setup_initial_position(self):
        """Set up the standard chess starting position"""
        # Place pawns
        for col in range(8):
            self.set_piece_at(1, col, Pawn(BLACK_PIECE, (1, col)))
            self.set_piece_at(6, col, Pawn(WHITE_PIECE, (6, col)))
        
        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col, piece_class in enumerate(piece_order):
            self.set_piece_at(0, col, piece_class(BLACK_PIECE, (0, col)))
            self.set_piece_at(7, col, piece_class(WHITE_PIECE, (7, col)))
        
    def get_piece_at(self, row, col):
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece_at(self, row, col, piece):
        """Place piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
            if piece:
                piece.position = (row, col)
    
    def move_piece(self, from_pos, to_pos):
        """Move piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.get_piece_at(from_row, from_col)
        if piece:
            self.set_piece_at(to_row, to_col, piece)
            self.set_piece_at(from_row, from_col, None)
            piece.move_to((to_row, to_col))
            self.switch_player()
            return True
        return False
    
    def switch_player(self):
        """Switch current player"""
        self.current_player = BLACK_PIECE if self.current_player == WHITE_PIECE else WHITE_PIECE
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def select_piece(self, row, col):
        """Select a piece and show valid moves"""
        piece = self.get_piece_at(row, col)
        
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.selected_position = (row, col)
            self.valid_moves = piece.get_valid_moves(self)
        else:
            self.clear_selection()
    
    def clear_selection(self):
        """Clear current selection"""
        self.selected_piece = None
        self.selected_position = None
        self.valid_moves = []
    
    def make_move(self, to_row, to_col):
        """Attempt to make a move to the specified position"""
        if self.selected_piece and (to_row, to_col) in self.valid_moves:
            self.move_piece(self.selected_position, (to_row, to_col))
            self.clear_selection()
            return True
        return False
```

**Key Board Features:**
- **2D Array Representation**: 8x8 grid storing piece objects
- **Initial Setup**: Places all pieces in standard starting positions
- **Move Validation**: Checks if moves are legal
- **Turn Management**: Alternates between white and black players
- **Selection System**: Tracks selected piece and valid moves

---

## 6. User Interface

### Step 6.1: Implement Renderer

Create `src/ui/renderer.py`:

```python
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create piece symbols for text rendering (fallback if no images)
        self.piece_symbols = {
            (WHITE_PIECE, KING): '♔',
            (WHITE_PIECE, QUEEN): '♕',
            (WHITE_PIECE, ROOK): '♖',
            (WHITE_PIECE, BISHOP): '♗',
            (WHITE_PIECE, KNIGHT): '♘',
            (WHITE_PIECE, PAWN): '♙',
            (BLACK_PIECE, KING): '♚',
            (BLACK_PIECE, QUEEN): '♛',
            (BLACK_PIECE, ROOK): '♜',
            (BLACK_PIECE, BISHOP): '♝',
            (BLACK_PIECE, KNIGHT): '♞',
            (BLACK_PIECE, PAWN): '♟',
        }
    
    def draw_board(self, board):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                
                # Calculate square position
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                
                # Draw square
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if board.selected_position == (row, col):
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Highlight valid moves
                if (row, col) in board.valid_moves:
                    pygame.draw.circle(self.screen, VALID_MOVE_COLOR, 
                                     (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), 10)
    
    def draw_pieces(self, board):
        """Draw all pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece:
                    self.draw_piece(piece, row, col)
    
    def draw_piece(self, piece, row, col):
        """Draw a single piece"""
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        
        # Use text symbols for pieces (can be replaced with images later)
        symbol = self.piece_symbols.get((piece.color, piece.get_piece_type()), '?')
        text_color = BLACK if piece.is_white() else BLACK
        
        text_surface = self.font.render(symbol, True, text_color)
        text_rect = text_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
        self.screen.blit(text_surface, text_rect)
    
    def draw_ui(self, board):
        """Draw game UI elements"""
        # Draw current player indicator
        player_text = f"Current Player: {board.current_player.title()}"
        text_surface = self.small_font.render(player_text, True, BLACK)
        self.screen.blit(text_surface, (BOARD_WIDTH + 10, 10))
        
        # Draw coordinates
        self.draw_coordinates()
        
        # Draw instructions
        instructions = [
            "Controls:",
            "R - Reset Game",
            "ESC - Quit",
            "",
            "Click piece to select",
            "Click destination to move"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(text_surface, (BOARD_WIDTH + 10, 50 + i * 25))
    
    def draw_coordinates(self):
        """Draw file and rank labels"""
        # Files (a-h)
        for col in range(8):
            letter = chr(ord('a') + col)
            text_surface = self.small_font.render(letter, True, BLACK)
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2 - text_surface.get_width() // 2
            self.screen.blit(text_surface, (x, BOARD_HEIGHT + 5))
        
        # Ranks (1-8)
        for row in range(8):
            number = str(8 - row)
            text_surface = self.small_font.render(number, True, BLACK)
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2 - text_surface.get_height() // 2
            self.screen.blit(text_surface, (BOARD_WIDTH + 5, y))
```

### Step 6.2: Implement Input Handler

Create `src/ui/input_handler.py`:

```python
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import *

class InputHandler:
    def __init__(self):
        pass
    
    def handle_click(self, mouse_pos, board):
        """Handle mouse click events"""
        x, y = mouse_pos
        
        # Check if click is within the board
        if x < BOARD_WIDTH and y < BOARD_HEIGHT:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            
            # If a piece is already selected, try to move it
            if board.selected_piece:
                if board.make_move(row, col):
                    # Move was successful
                    pass
                else:
                    # Move failed, try selecting new piece
                    board.select_piece(row, col)
            else:
                # No piece selected, try to select one
                board.select_piece(row, col)
    
    def get_square_from_mouse(self, mouse_pos):
        """Convert mouse position to board coordinates"""
        x, y = mouse_pos
        if x < BOARD_WIDTH and y < BOARD_HEIGHT:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            return (row, col)
        return None
```

### Step 6.3: Create UI Module

Create `src/ui/__init__.py`:

```python
import os
import sys

# Add current directory to path so we can import from same directory
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

from renderer import Renderer
from input_handler import InputHandler

__all__ = ['Renderer', 'InputHandler']
```

---

## 7. Game Logic

### Step 7.1: Create Move Class

Create `src/move.py`:

```python
"""
Move class for representing chess moves
"""

class Move:
    def __init__(self, from_pos, to_pos, piece, captured_piece=None, special_move=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured_piece = captured_piece
        self.special_move = special_move  # For castling, en passant, etc.
    
    def __str__(self):
        return f"{self.piece} from {self.from_pos} to {self.to_pos}"
    
    def __repr__(self):
        return self.__str__()
    
    def get_algebraic_notation(self):
        """Convert move to standard chess algebraic notation"""
        # TODO: Implement proper algebraic notation
        from_file = chr(ord('a') + self.from_pos[1])
        from_rank = str(8 - self.from_pos[0])
        to_file = chr(ord('a') + self.to_pos[1])
        to_rank = str(8 - self.to_pos[0])
        
        return f"{from_file}{from_rank}{to_file}{to_rank}"
```

### Step 7.2: Implement Main Game Class

Create `src/game.py`:

```python
import pygame
from board import Board
from constants import *
from ui.renderer import Renderer
from ui.input_handler import InputHandler

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        
        self.board = Board()
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler()
        
        self.running = True
        self.game_over = False
        self.winner = None
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    self.input_handler.handle_click(mouse_pos, self.board)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        # TODO: Add game logic updates like check/checkmate detection
        pass
    
    def render(self):
        """Render the game"""
        self.screen.fill(WHITE)
        self.renderer.draw_board(self.board)
        self.renderer.draw_pieces(self.board)
        self.renderer.draw_ui(self.board)
        pygame.display.flip()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.game_over = False
        self.winner = None
```

### Step 7.3: Create Main Entry Point

Create `src/main.py`:

```python
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
```

### Step 7.4: Create Main Package Init

Create `src/__init__.py`:

```python
"""
Chess Game Package
A simple chess game implementation using pygame.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
```

---

## 8. Testing

### Step 8.1: Create Board Tests

Create `tests/test_board.py`:

```python
import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from board import Board
from pieces import Pawn, Rook, King
from constants import WHITE_PIECE, BLACK_PIECE

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Set up test board before each test"""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test that board initializes correctly"""
        self.assertEqual(self.board.current_player, WHITE_PIECE)
        self.assertIsNone(self.board.selected_piece)
        self.assertEqual(len(self.board.valid_moves), 0)
    
    def test_initial_piece_placement(self):
        """Test that pieces are placed correctly at start"""
        # Test white pawns
        for col in range(8):
            piece = self.board.get_piece_at(6, col)
            self.assertIsInstance(piece, Pawn)
            self.assertEqual(piece.color, WHITE_PIECE)
        
        # Test black pawns
        for col in range(8):
            piece = self.board.get_piece_at(1, col)
            self.assertIsInstance(piece, Pawn)
            self.assertEqual(piece.color, BLACK_PIECE)
        
        # Test white king
        king = self.board.get_piece_at(7, 4)
        self.assertIsInstance(king, King)
        self.assertEqual(king.color, WHITE_PIECE)
    
    def test_piece_movement(self):
        """Test basic piece movement"""
        # Move white pawn
        self.board.select_piece(6, 4)  # Select white pawn
        self.assertTrue(self.board.make_move(4, 4))  # Move two squares
        
        # Check piece moved
        piece = self.board.get_piece_at(4, 4)
        self.assertIsInstance(piece, Pawn)
        self.assertEqual(piece.color, WHITE_PIECE)
        
        # Check old position is empty
        self.assertIsNone(self.board.get_piece_at(6, 4))
    
    def test_turn_switching(self):
        """Test that turns switch correctly"""
        self.assertEqual(self.board.current_player, WHITE_PIECE)
        
        # Make a move
        self.board.select_piece(6, 4)
        self.board.make_move(4, 4)
        
        # Player should switch
        self.assertEqual(self.board.current_player, BLACK_PIECE)

if __name__ == '__main__':
    unittest.main()
```

### Step 8.2: Create Piece Tests

Create `tests/test_pieces.py`:

```python
import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from board import Board
from constants import WHITE_PIECE, BLACK_PIECE

class TestPieces(unittest.TestCase):
    def setUp(self):
        """Set up test board before each test"""
        self.board = Board()
    
    def test_pawn_initial_moves(self):
        """Test pawn can move 1 or 2 squares initially"""
        pawn = self.board.get_piece_at(6, 4)  # White pawn
        moves = pawn.get_valid_moves(self.board)
        
        # Should be able to move 1 or 2 squares forward
        self.assertIn((5, 4), moves)
        self.assertIn((4, 4), moves)
        self.assertEqual(len(moves), 2)
    
    def test_pawn_single_move_after_first(self):
        """Test pawn can only move 1 square after first move"""
        # Move pawn first
        self.board.move_piece((6, 4), (5, 4))
        pawn = self.board.get_piece_at(5, 4)
        moves = pawn.get_valid_moves(self.board)
        
        # Should only be able to move 1 square
        self.assertIn((4, 4), moves)
        self.assertNotIn((3, 4), moves)
        self.assertEqual(len(moves), 1)
    
    def test_rook_moves(self):
        """Test rook moves horizontally and vertically"""
        # Clear path for rook
        self.board.set_piece_at(7, 1, None)  # Remove knight
        self.board.set_piece_at(6, 0, None)  # Remove pawn
        
        rook = self.board.get_piece_at(7, 0)
        moves = rook.get_valid_moves(self.board)
        
        # Should be able to move up the file and along the rank
        self.assertIn((6, 0), moves)
        self.assertIn((5, 0), moves)
        self.assertIn((7, 1), moves)
    
    def test_knight_moves(self):
        """Test knight L-shaped moves"""
        knight = self.board.get_piece_at(7, 1)
        moves = knight.get_valid_moves(self.board)
        
        # Knight should have 2 valid moves from starting position
        self.assertIn((5, 0), moves)
        self.assertIn((5, 2), moves)
        self.assertEqual(len(moves), 2)
    
    def test_king_moves(self):
        """Test king one-square moves"""
        # Clear space around king
        self.board.set_piece_at(6, 3, None)
        self.board.set_piece_at(6, 4, None)
        self.board.set_piece_at(6, 5, None)
        
        king = self.board.get_piece_at(7, 4)
        moves = king.get_valid_moves(self.board)
        
        # King should be able to move to adjacent squares
        self.assertIn((6, 4), moves)
        self.assertTrue(len(moves) > 0)

if __name__ == '__main__':
    unittest.main()
```

### Step 8.3: Create Simple Validation Script

Create `validate.py` in the root directory:

```python
import os
import sys

# Change to src directory and add to path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
os.chdir(src_dir)
sys.path.insert(0, src_dir)

print("Testing chess game...")

try:
    from board import Board
    print("✓ Board import successful")
    
    board = Board()
    print("✓ Board created successfully")
    
    # Check if pieces are placed
    piece = board.get_piece_at(6, 4)
    print(f"✓ Piece at (6,4): {piece}")
    
    # Test selection
    board.select_piece(6, 4)
    print(f"✓ Selected piece, valid moves: {len(board.valid_moves)}")
    
    print("\n🎉 Chess game is working correctly!")
    print("\nTo play the game, run:")
    print("cd chess_game/src && python3 main.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## 9. Running the Game

### Step 9.1: Final Testing

```bash
# Test the game components
cd chess_game
python3 validate.py

# Run unit tests (if pytest is installed)
python3 -m unittest tests.test_board tests.test_pieces -v

# Or run tests individually
cd src
python3 -c "from board import Board; print('✓ Board works'); from pieces import *; print('✓ Pieces work')"
```

### Step 9.2: Run the Game

```bash
cd chess_game/src
python3 main.py
```

### Step 9.3: Game Controls

- **Left Click**: Select a piece or move to a square
- **R Key**: Reset the game
- **ESC Key**: Quit the game

---

## 10. Architecture Overview

### Design Patterns Used

1. **Model-View-Controller (MVC)**:
   - Model: `Board`, `Piece` classes
   - View: `Renderer` class
   - Controller: `Game`, `InputHandler` classes

2. **Strategy Pattern**: 
   - Each piece type implements its own movement strategy

3. **Template Method Pattern**:
   - Base `Piece` class defines common interface
   - Subclasses implement specific behavior

### Key Components

1. **Game Engine** (`game.py`):
   - Main game loop
   - Event handling
   - Game state management

2. **Board Management** (`board.py`):
   - Piece positioning
   - Move validation
   - Turn management

3. **Piece Logic** (`pieces/`):
   - Individual piece movement rules
   - Inheritance hierarchy

4. **User Interface** (`ui/`):
   - Rendering system
   - Input processing

### Future Enhancements

1. **Advanced Chess Rules**:
   - Check/checkmate detection
   - Castling
   - En passant
   - Pawn promotion

2. **AI Opponent**:
   - Minimax algorithm
   - Alpha-beta pruning
   - Position evaluation

3. **Enhanced UI**:
   - Piece images instead of Unicode
   - Sound effects
   - Animation system
   - Menu system

4. **Game Features**:
   - Save/load games
   - Move history
   - Undo/redo functionality
   - Online multiplayer

This step-by-step guide provides a complete foundation for building a chess game. Each component is modular and can be extended or modified independently.
