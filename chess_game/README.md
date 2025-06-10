# Chess Game

A beautiful, modern chess game implementation using Python and Pygame with enhanced UI.

## ✨ Features

### 🎮 Core Gameplay
- Complete chess board with all pieces
- Standard chess piece movement rules
- Turn-based gameplay
- Move validation and game logic
- Game reset functionality

### 🎨 Beautiful UI & Graphics
- **Modern gradient backgrounds** with professional styling
- **Elegant color palette** with cream and brown chess squares
- **Enhanced piece rendering** with two modes:
  - Solid white/black pieces with contrasting outlines
  - Pieces on colored circular backgrounds
- **Smooth 60 FPS animations** with pulsing highlights
- **Professional UI panels** with rounded corners
- **Visual feedback** for selections and valid moves
- **Coordinate labels** with elegant styling

### 🖱️ Interactive Interface
- Click-to-select and click-to-move interface
- **Animated highlights** for selected pieces
- **Green indicators** for valid moves
- **Hover effects** and visual feedback
- Keyboard shortcuts (R to reset, ESC to quit)

## Project Structure

```
chess_game/
├── assets/
│   ├── images/
│   │   └── pieces/          # For future piece images
│   └── sounds/              # For future sound effects
├── src/
│   ├── main.py             # Game entry point
│   ├── game.py             # Main game loop and logic
│   ├── board.py            # Chess board representation
│   ├── constants.py        # Game constants and settings
│   ├── move.py             # Move representation
│   ├── pieces/             # Chess piece implementations
│   │   ├── piece.py        # Base piece class
│   │   ├── pawn.py         # Pawn piece
│   │   ├── rook.py         # Rook piece
│   │   ├── knight.py       # Knight piece
│   │   ├── bishop.py       # Bishop piece
│   │   ├── queen.py        # Queen piece
│   │   └── king.py         # King piece
│   └── ui/                 # User interface components
│       ├── renderer.py     # Game rendering
│       └── input_handler.py # Input processing
├── tests/                  # Unit tests
└── requirements.txt        # Python dependencies
```

## Installation

1. Make sure you have Python 3.6+ installed
2. Install pygame:
   ```bash
   pip3 install pygame
   ```
   Or install from requirements.txt:
   ```bash
   pip3 install -r requirements.txt
   ```

## How to Run

```bash
cd chess_game/src
python3 main.py
```

> **🎨 New!** Pieces now feature solid white and black colors for clear differentiation. See `PIECE_COLORS_REFERENCE.md` for rendering options.

## Controls

- **Mouse Click**: Select a piece or move to a square
- **R**: Reset the game
- **ESC**: Quit the game

## How to Play

1. White moves first
2. Click on a piece to select it (pieces show available moves in green)
3. Click on a highlighted square to move the piece
4. The game alternates between white and black turns
5. Follow standard chess rules

## Chess Pieces

- **♔/♚** King - Moves one square in any direction
- **♕/♛** Queen - Moves any distance horizontally, vertically, or diagonally
- **♖/♜** Rook - Moves any distance horizontally or vertically
- **♗/♝** Bishop - Moves any distance diagonally
- **♘/♞** Knight - Moves in an L-shape (2+1 squares)
- **♙/♟** Pawn - Moves forward one square, captures diagonally

## Current Status

✅ **Implemented:**
- Complete board setup
- All piece types with basic movement
- Turn-based gameplay
- Visual feedback for valid moves
- Basic game loop

🚧 **Future Enhancements:**
- Check/checkmate detection
- Castling
- En passant
- Pawn promotion
- Game state saving/loading
- AI opponent
- Sound effects
- Better graphics

## Development

To run tests:
```bash
cd chess_game/src
python3 -c "from board import Board; print('✓ Board works'); from pieces import *; print('✓ Pieces work')"
```

## License

MIT License - see LICENSE file for details.

## Contributing

Feel free to contribute improvements, bug fixes, or new features!

## Piece Rendering

The game features two rendering methods for optimal piece visibility:

### Method 1: Outline Text (Default)
- White pieces: Solid white symbols with black outline
- Black pieces: Solid black symbols with white outline
- Classic chess appearance with excellent contrast

### Method 2: Background Circles
- White pieces: Black symbols on white circular backgrounds
- Black pieces: White symbols on black circular backgrounds
- Maximum visibility and modern appearance

To switch rendering methods, edit `src/constants.py`:
```python
USE_BACKGROUND_CIRCLES = False  # Outline method (default)
USE_BACKGROUND_CIRCLES = True   # Background circles method
```
