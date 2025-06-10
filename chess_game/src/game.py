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
                elif event.key == pygame.K_z:
                    # Undo last move with Z key
                    self.board.undo_move()
    
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
                self.board.game_status = "Game in progress"
    
    def render(self):
        """Render the game using enhanced renderer"""
        self.renderer.render(self.board)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.game_over = False
        self.winner = None