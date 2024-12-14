import numpy as np
from board import Board

class Board_With_History(Board):
    def __init__(self, b = None) -> None:
        if b is None:
            self.x = 0              # Bitboard for X pieces
            self.o = 0              # Bitboard for X pieces
            self.xinhand = 9        # Number of unplayed X pieces
            self.oinhand = 9        # Number of unplayed O pieces
            self.xmove = True       # X to move?
            self.history = []
        else:
            self.x = b.x               # Bitboard for X pieces
            self.o = b.o               # Bitboard for X pieces
            self.xinhand = b.xinhand   # Number of unplayed X pieces
            self.oinhand = b.oinhand  # Number of unplayed O pieces
            self.xmove = b.xmove      # X to move?
            self.history = b.history

    def save_state_to_history(self) -> None:
        self.history.append(Board(self))

    def is_equal(self, b:Board) -> bool:
        return self.x==b.x and self.o==b.o and self.xinhand==b.xinhand and self.oinhand==b.oinhand and self.xmove==b.xmove
    
    def get_board_at_move(self, move_number:int) -> Board | None:
        if move_number<0 or move_number>=len(self.history):
            return None
        return self.history[move_number]
    
    def check_for_repetition(self) -> bool:
        for b in self.history[:-1]:
            if self.is_equal(b):
                return True
        return False
    
    def game_loop(self) -> None:
        self.save_state_to_history()
        super().game_loop()