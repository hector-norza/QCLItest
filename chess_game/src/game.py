import pygame
import threading
import time
from board import Board
from constants import *
from ui.renderer import Renderer
from ui.input_handler import InputHandler
from ai_player import AIPlayer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        
        self.board = Board()
        self.renderer = Renderer(self.screen)
        self.renderer.game = self  # Give renderer a reference to the game
        self.input_handler = InputHandler()
        
        # AI settings
        self.use_ai = False  # Default to human vs human
        self.ai_player = AIPlayer(difficulty='medium')
        self.ai_color = BLACK_PIECE  # AI plays as black by default
        self.ai_thread = None
        
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
                # Only handle clicks if it's not AI's turn or AI is not thinking
                if not (self.use_ai and self.board.current_player == self.ai_color) and not self.board.ai_thinking:
                    if event.button == 1:  # Left click
                        mouse_pos = pygame.mouse.get_pos()
                        self.input_handler.handle_click(mouse_pos, self.board)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_z:
                    # Undo last move with Z key (undo twice if playing against AI)
                    if self.use_ai:
                        # Undo both AI's move and player's move
                        self.board.undo_move()
                        if self.board.current_player == self.ai_color:
                            self.board.undo_move()
                    else:
                        self.board.undo_move()
                elif event.key == pygame.K_a:
                    # Toggle AI opponent with A key
                    self.toggle_ai()
                elif event.key == pygame.K_d:
                    # Cycle AI difficulty with D key
                    self.cycle_ai_difficulty()
    
    def update(self):
        """Update game state"""
        # Check for checkmate or stalemate
        if not self.game_over:
            if self.board.is_checkmate(self.board.current_player):
                self.game_over = True
                winner = "White" if self.board.current_player == BLACK_PIECE else "Black"
                self.winner = winner
                self.board.game_status = f"{winner} wins by checkmate!"
            elif self.board.is_stalemate(self.board.current_player):
                self.game_over = True
                self.board.game_status = "Draw by stalemate!"
            elif self.board.is_in_check(self.board.current_player):
                self.board.game_status = f"{self.board.current_player.capitalize()} is in check!"
            else:
                if self.board.ai_thinking:
                    self.board.game_status = "AI is thinking..."
                else:
                    self.board.game_status = "Game in progress"
            
            # Check if it's AI's turn
            if (self.use_ai and 
                self.board.current_player == self.ai_color and 
                not self.game_over and 
                not self.board.ai_thinking and
                self.ai_thread is None):
                self.board.ai_thinking = True
                self.ai_thread = threading.Thread(target=self._make_ai_move)
                self.ai_thread.daemon = True
                self.ai_thread.start()
    
    def _make_ai_move(self):
        """Make an AI move in a separate thread"""
        # Add a small delay to make the AI seem like it's thinking
        time.sleep(0.5)
        
        # Get AI's move
        move = self.ai_player.get_move(self.board)
        
        if move:
            from_pos, to_pos = move
            
            # Select the piece
            row, col = from_pos
            self.board.select_piece(row, col)
            
            # Make the move
            to_row, to_col = to_pos
            self.board.make_move(to_row, to_col)
        
        # Reset AI thinking flags
        self.board.ai_thinking = False
        self.ai_thread = None
    
    def render(self):
        """Render the game using enhanced renderer"""
        self.renderer.render(self.board)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.game_over = False
        self.winner = None
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.game_over = False
        self.winner = None
        
        # If AI is enabled and it's black's turn, make AI move
        if self.use_ai and self.board.current_player == self.ai_color:
            self.board.ai_thinking = True
            self.ai_thread = threading.Thread(target=self._make_ai_move)
            self.ai_thread.daemon = True
            self.ai_thread.start()
    
    def toggle_ai(self):
        """Toggle AI opponent on/off"""
        self.use_ai = not self.use_ai
        
        # If turning on AI and it's AI's turn, make a move
        if self.use_ai and self.board.current_player == self.ai_color and not self.game_over:
            self.board.ai_thinking = True
            self.ai_thread = threading.Thread(target=self._make_ai_move)
            self.ai_thread.daemon = True
            self.ai_thread.start()
    
    def cycle_ai_difficulty(self):
        """Cycle through AI difficulty levels"""
        if self.ai_player.difficulty == 'easy':
            self.ai_player.difficulty = 'medium'
        elif self.ai_player.difficulty == 'medium':
            self.ai_player.difficulty = 'hard'
        else:
            self.ai_player.difficulty = 'easy'