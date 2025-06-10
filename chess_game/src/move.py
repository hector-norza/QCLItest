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