from player import Player
from board import Board
import random

class Player_Random(Player):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
    
    def get_placement(self, board: Board) -> list[int, int]:
        """Place a piece on a random empty tile."""
        options = board.get_empty_tiles()
        i,j = random.choice(options)
        return [i,j]
    
    def get_move(self, board: Board) -> list[int, int, int, int]:
        """Make a random move."""
        o_options = [(i,j) for (i,j) in board.get_os() if board.rock_has_move(i,j)]
        x_options = [(i,j) for (i,j) in board.get_xs() if board.rock_has_move(i,j)]
        piece_options = x_options if board.xmove else o_options
        i,j = random.choice(piece_options)
        move_options = board.get_possible_moves(i,j)
        ii,jj = random.choice(move_options)
        return [i,j,ii,jj]
    
    def get_removal(self, board: Board) -> list[int, int]:
        """Remove a random opponents piece."""
        o_options = [(i,j) for (i,j) in board.get_os() if not board.is_in_mill(i,j)]
        x_options = [(i,j) for (i,j) in board.get_xs() if not board.is_in_mill(i,j)]
        if board.xmove:
            print(f'x options: {x_options}')
        else:
            print(f'o options: {o_options}')
        options = o_options if board.xmove else x_options
        i,j = random.choice(options)
        print(f'chosen ({i},{j})')
        return [i,j]