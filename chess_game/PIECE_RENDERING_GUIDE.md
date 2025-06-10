# Chess Piece Rendering Guide

## Overview
Your chess game now has two rendering methods for better piece differentiation:

## Method 1: Outline Text (Default)
- **White pieces**: Solid white text with black outline
- **Black pieces**: Solid black text with white outline
- Clean, classic appearance
- Good contrast on any board color

## Method 2: Background Circles
- **White pieces**: Black text on white circular background
- **Black pieces**: White text on black circular background  
- Maximum contrast and visibility
- Modern, distinctive look

## How to Switch Rendering Methods

### Option 1: Edit Constants File
In `src/constants.py`, change the line:
```python
USE_BACKGROUND_CIRCLES = False  # For outline method
USE_BACKGROUND_CIRCLES = True   # For background circles
```

### Option 2: Quick Test Both Methods
Run this command to test with background circles:
```bash
cd chess_game/src
python3 -c "
import constants
constants.USE_BACKGROUND_CIRCLES = True
from game import Game
game = Game()
game.run()
"
```

## Visual Differences

### Current Setup (Outline Method):
- ♔ White King: White symbol with black border
- ♚ Black King: Black symbol with white border
- All pieces maintain their Unicode chess symbols
- Crisp, traditional chess appearance

### Alternative Setup (Background Circles):
- ♔ White King: Black symbol on white circle with black border
- ♚ Black King: White symbol on black circle with white border
- Enhanced visibility on any background
- Modern, game-like appearance

## Recommendation
- Use **Outline Method** for traditional chess feel
- Use **Background Circles** for maximum visibility or modern look

The game is currently set to use the **Outline Method** by default, which provides excellent contrast between white and black pieces while maintaining the classic chess aesthetic.
