# Chess Game Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Create Project Structure
```bash
mkdir chess_game && cd chess_game
mkdir -p {assets/{images/pieces,sounds},src/{pieces,ui},tests}
```

### 2. Install Dependencies
```bash
echo "pygame==2.5.2" > requirements.txt
pip3 install -r requirements.txt
```

### 3. Create Core Files (Copy & Paste Ready)

#### Constants (`src/constants.py`)
```python
import pygame

BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_WIDTH = BOARD_SIZE * SQUARE_SIZE
BOARD_HEIGHT = BOARD_SIZE * SQUARE_SIZE
WINDOW_WIDTH = BOARD_WIDTH + 200
WINDOW_HEIGHT = BOARD_HEIGHT + 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)
VALID_MOVE_COLOR = (0, 255, 0, 128)

WHITE_PIECE = 'white'
BLACK_PIECE = 'black'

PAWN = 'pawn'
ROOK = 'rook'
KNIGHT = 'knight'
BISHOP = 'bishop'
QUEEN = 'queen'
KING = 'king'
```

#### Run the Game
```bash
cd src
python3 main.py
```

## 📋 Development Checklist

### Core Components
- [ ] Constants and configuration
- [ ] Base Piece class (abstract)
- [ ] Individual piece classes (6 pieces)
- [ ] Board class with game logic
- [ ] Renderer for graphics
- [ ] Input handler for controls
- [ ] Main game loop
- [ ] Entry point script

### Chess Pieces Implementation Order
1. [ ] **Piece** (base class) - Abstract methods
2. [ ] **Pawn** - Forward movement, diagonal capture
3. [ ] **Rook** - Horizontal/vertical lines
4. [ ] **Bishop** - Diagonal lines  
5. [ ] **Knight** - L-shaped moves
6. [ ] **Queen** - Rook + Bishop moves
7. [ ] **King** - One square in any direction

### Game Features
- [ ] Piece selection with highlighting
- [ ] Valid move visualization
- [ ] Turn-based gameplay
- [ ] Move validation
- [ ] Game reset functionality
- [ ] Coordinate display

## 🎮 Controls
- **Click**: Select piece / Make move
- **R**: Reset game
- **ESC**: Quit

## 🔧 Testing Commands

```bash
# Test imports
cd src && python3 -c "from board import Board; print('✓ Works')"

# Test piece creation
python3 -c "from pieces import *; print('✓ All pieces imported')"

# Test board setup
python3 -c "from board import Board; b=Board(); print(f'✓ {sum(1 for row in b.board for p in row if p)} pieces')"

# Run the game
python3 main.py
```

## 📁 File Structure
```
chess_game/
├── src/
│   ├── main.py           # Entry point
│   ├── game.py           # Game loop
│   ├── board.py          # Board logic
│   ├── constants.py      # Settings
│   ├── pieces/           # All chess pieces
│   └── ui/              # Rendering & input
├── tests/               # Unit tests
└── requirements.txt     # Dependencies
```

## 🚨 Common Issues & Solutions

### Import Errors
```bash
# Fix: Run from src directory
cd src && python3 main.py
```

### Pygame Not Found
```bash
pip3 install pygame
```

### Module Not Found
```bash
# Add path in Python files:
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
```

## 🎯 Next Steps After Basic Game

1. **Enhanced Rules**: Check/checkmate, castling, en passant
2. **AI Player**: Minimax algorithm with alpha-beta pruning
3. **Better Graphics**: Piece images, animations, themes
4. **Game Features**: Save/load, move history, analysis
5. **Multiplayer**: Network play, online chess server

## 📚 Key Learning Concepts

- **Object-Oriented Design**: Inheritance, polymorphism
- **Game Programming**: Game loops, event handling
- **Chess Logic**: Piece movements, board representation
- **Python Modules**: Package structure, imports
- **Testing**: Unit tests, validation scripts

This guide gets you from zero to a working chess game in under an hour!
