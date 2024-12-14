import pygame
import numpy as np
from board_visual import Board_Visual  # Assuming Board is your original class

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_COLOR = (255, 0, 0)  # Red for X
O_COLOR = (0, 0, 255)  # Blue for O
X_MILL_COLOR = (255, 100, 100)  # Red for X
O_MILL_COLOR = (100, 100, 255)  # Blue for O
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for highlights
LAST_MOVE_COLOR = (200, 200, 0)  # Color for last move

# Board_Visual class
class Board_Visual_With_History(Board_Visual):
    def __init__(self, b = None):
        super().__init__(b)
        if b is None:
            self.history = []
        else:
            self.history = b.history

    def save_state_to_history(self) -> None:
        b = Board_Visual(self)
        self.history.append(Board_Visual(self))

    def is_equal(self, b:Board_Visual) -> bool:
        return self.x==b.x and self.o==b.o and self.xinhand==b.xinhand and self.oinhand==b.oinhand and self.xmove==b.xmove
    
    def get_board_at_move(self, move_number:int) -> Board_Visual | None:
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