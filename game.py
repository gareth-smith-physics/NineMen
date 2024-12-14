import numpy as np
from board_with_history import Board_With_History
from player import Player
from player_human import Human

class Game:
    def __init__(self, p1: Player, p2: Player) -> None:
        self.isremove = False   # The next move is a removal
        self.p1 = p1            # Player 1
        self.p2 = p2            # Player 2
        self.board = Board_With_History()    # The board        
        self.verbose = False

    def place(self, i: int, j: int) -> bool:
        """Place a piece on the board for the current player."""
        in_hand = self.board.xinhand if self.board.xmove else self.board.oinhand
        if self.isremove or in_hand <= 0 or not self.board.is_empty(i, j):
            return False
        if self.board.xmove:
            self.board.add_x(i,j)
            if self.verbose:
                print(f'Placed an X on ({i},{j})')
        else:
            self.board.add_o(i,j)
            if self.verbose:
                print(f'Placed an O on ({i},{j})')
        if self.board.is_in_mill(i, j):
            self.isremove = True
            if self.verbose:
                print(f'Mill formed! Remove a piece...')
        else:
            self.board.xmove = not self.board.xmove
        return True

    def remove(self, i: int, j: int) -> bool:
        """Remove the opponent's piece."""
        if not self.isremove:
            return False
        if self.board.xmove:
            if not self.board.is_o(i, j) or (self.board.is_in_mill(i, j) and self.board.o_out_of_mill()):
                return False
            self.board.remove_o(i,j)
            if self.verbose:
                print(f'Removed an O on ({i},{j})')
        else:
            if not self.board.is_x(i, j) or (self.board.is_in_mill(i, j) and self.board.x_out_of_mill()):
                return False
            self.board.remove_x(i,j)
            if self.verbose:
                print(f'Removed an X on ({i},{j})')
        self.isremove = False
        self.board.xmove = not self.board.xmove
        return True

    def move(self, i: int, j: int, ii: int, jj: int) -> bool:
        """Move a piece on the board."""
        if self.isremove or (self.board.xmove and self.board.xinhand > 0) or (not self.board.xmove and self.board.oinhand > 0):
            if self.verbose:
                print(f'Tried to move at wrong time')
            return False
        getter = self.board.is_x if self.board.xmove else self.board.is_o
        mover = self.board.move_x if self.board.xmove else self.board.move_o
        if not getter(i,j):
            if self.verbose:
                print(f'No piece on ({i},{j}), cant move')
            return False
        if not self.board.is_empty(ii, jj):
            if self.verbose:
                print(f'({ii},{jj}) is already occupied, cant move')
            return False
        if not self.board.is_connected(i,j, ii, jj) and ((self.board.count_x_on_board()>3) if self.board.xmove else (self.board.count_o_on_board()>3)):
            if self.verbose:
                print(f'({ii},{jj}) is not adjacent to ({i},{j}), cant move')
            return False
        mover(i,j,ii,jj)
        if self.verbose:
            print(f'Moved ({i},{j}) to ({ii},{jj})')
        if self.board.is_in_mill(ii, jj):
            self.isremove = True
        else:
            self.board.xmove = not self.board.xmove
        return True

    def xWins(self) -> None:
        if self.verbose:
            print(f"{self.p1.name} (X) wins!")
        self.p1.end_game(1)
        self.p2.end_game(-1)

    def oWins(self) -> None:
        if self.verbose:
            print(f"{self.p2.name} (O) wins!")
        self.p1.end_game(-1)
        self.p2.end_game(1)

    def tie(self) -> None:
        if self.verbose:
            print(f"Tie game!")
        self.p1.end_game(0)
        self.p2.end_game(0)


    def game_loop(self) -> None:
        """Main game loop."""
        while True:
            self.board.print_board()
            moved = False
            if self.board.check_winner()==1:
                self.xWins()
                return
            if self.board.check_winner()==-1:
                self.oWins()
                return
            if self.board.check_for_repetition():
                self.tie()
                return
            player = self.p1 if self.board.xmove else self.p2
            if self.isremove:
                i, j = player.get_removal(self.board)
                moved = self.remove(i, j)
            elif self.board.xmove and self.board.xinhand > 0 or not self.board.xmove and self.board.oinhand > 0:
                i, j = player.get_placement(self.board)
                moved = self.place(i, j)
            else:
                i, j, ii, jj = player.get_move(self.board)
                moved = self.move(i, j, ii, jj)
            if moved:
                self.board.save_state_to_history()
