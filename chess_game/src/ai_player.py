"""
AI Player for Chess Game
Implements a simple AI that can play chess
"""

import random
from constants import *

class AIPlayer:
    def __init__(self, difficulty='medium'):
        """Initialize AI player with a difficulty level"""
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'
    
    def get_move(self, board):
        """Get the AI's next move based on the current board state"""
        if self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            return self._get_smart_move(board)
        else:  # hard
            return self._get_smart_move(board, depth=2)
    
    def _get_random_move(self, board):
        """Make a completely random legal move"""
        # Get all pieces of the current player
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == board.current_player:
                    pieces.append((row, col, piece))
        
        # Shuffle pieces for randomness
        random.shuffle(pieces)
        
        # Try each piece until we find one with valid moves
        for row, col, piece in pieces:
            valid_moves = piece.get_valid_moves(board)
            if valid_moves:
                # Choose a random move
                to_pos = random.choice(valid_moves)
                return (row, col), to_pos
        
        # No valid moves found (shouldn't happen unless checkmate/stalemate)
        return None
    
    def _get_smart_move(self, board, depth=1):
        """Make a smarter move by evaluating piece values"""
        best_score = float('-inf')
        best_move = None
        
        # Get all pieces of the current player
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == board.current_player:
                    pieces.append((row, col, piece))
        
        # Try each piece and each of its moves
        for row, col, piece in pieces:
            valid_moves = piece.get_valid_moves(board)
            for to_pos in valid_moves:
                # Simulate the move
                score = self._evaluate_move(board, (row, col), to_pos, depth)
                
                # Keep track of the best move
                if score > best_score:
                    best_score = score
                    best_move = ((row, col), to_pos)
        
        return best_move
    
    def _evaluate_move(self, board, from_pos, to_pos, depth):
        """Evaluate a move by simulating it and scoring the resulting position"""
        # Create a copy of the board
        temp_board = board._simulate_move(from_pos, to_pos)
        
        # Base score: material advantage
        score = self._evaluate_material(temp_board)
        
        # Add positional scoring
        score += self._evaluate_position(temp_board)
        
        # Check for check/checkmate
        opponent_color = BLACK_PIECE if temp_board.current_player == WHITE_PIECE else WHITE_PIECE
        if temp_board.is_checkmate(opponent_color):
            score += 1000  # Big bonus for checkmate
        elif temp_board.is_in_check(opponent_color):
            score += 50    # Bonus for check
        
        # Look ahead if depth > 0
        if depth > 0:
            # Find the opponent's best response
            opponent_best_score = float('-inf')
            
            # Get all opponent pieces
            for row in range(8):
                for col in range(8):
                    piece = temp_board.get_piece_at(row, col)
                    if piece and piece.color == opponent_color:
                        valid_moves = piece.get_valid_moves(temp_board)
                        for next_pos in valid_moves:
                            # Evaluate opponent's move
                            response_score = -self._evaluate_move(temp_board, (row, col), next_pos, depth-1)
                            opponent_best_score = max(opponent_best_score, response_score)
            
            # Subtract opponent's best response from our score
            if opponent_best_score != float('-inf'):
                score -= opponent_best_score
        
        return score
    
    def _evaluate_material(self, board):
        """Evaluate material advantage on the board"""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece:
                    # Add piece value for our pieces, subtract for opponent's
                    value = PIECE_VALUES.get(piece.get_piece_type(), 0)
                    if piece.color == board.current_player:
                        score += value
                    else:
                        score -= value
        return score
    
    def _evaluate_position(self, board):
        """Evaluate positional advantages"""
        score = 0
        current_player = board.current_player
        
        # Bonus for controlling the center
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            piece = board.get_piece_at(row, col)
            if piece:
                if piece.color == current_player:
                    score += 3
                else:
                    score -= 3
        
        # Bonus for developed pieces (not in starting position)
        back_row = 7 if current_player == WHITE_PIECE else 0
        for col in range(8):
            piece = board.get_piece_at(back_row, col)
            if piece and piece.color == current_player and piece.has_moved:
                score += 2
        
        # Penalty for moving king early (except castling)
        king_moved = False
        for row in range(8):
            for col in range(8):
                piece = board.get_piece_at(row, col)
                if piece and piece.color == current_player and piece.get_piece_type() == KING:
                    if piece.has_moved and len(board.move_history) < 10:
                        # Check if it was a castling move
                        was_castling = False
                        for move in board.move_history:
                            if move.piece == piece and abs(move.from_pos[1] - move.to_pos[1]) == 2:
                                was_castling = True
                                break
                        
                        if not was_castling:
                            score -= 10
        
        return score