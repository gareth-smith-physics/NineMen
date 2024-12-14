from player import Player
from board_with_history import Board_With_History
import random
from database import Database
import numpy as np

class Player_AlphaBeta(Player):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.k_removal = -1
        self.database_3_3 = Database(db_name="positions_3-3.db")
        self.database_4_3 = Database(db_name="positions_4-3.db")
        self.database_4_4 = Database(db_name="positions_4-4.db")
        self.name = name
        self.prune = True
        self.max_depth = 2
        self.close_on_end = True
    
    def get_placement(self, board: Board_With_History) -> list[int, int]:
        """Place a piece on a random empty tile. This should never come up."""
        options = board.get_empty_tiles()
        i,j = random.choice(options)
        return [i,j]
    
    def get_move(self, board: Board_With_History) -> list[int, int, int, int]:
        """If the position is in the database, look it up.
        Otherwise, use minmax to find the best move, then add the position to the database."""
        (k_start, k_end, k_removal, outcome, calculated_depth) = self.calculate_best_move(board)
        if self.verbose:
            print(f'Verdict: {self.name+" wins." if (outcome>0 and self.isX) or (outcome<0 and not self.isX) else self.name+" loses." if (outcome<0 and self.isX) or (outcome>0 and not self.isX) else "Draw"} (outcome {outcome}, depth {calculated_depth})')
        self.k_removal = k_removal
        return [k_start//8, k_start%8, k_end//8, k_end%8]

    def calculate_best_move(self, board: Board_With_History) -> tuple[int, int, int, int, int]:
        database = (self.database_3_3 if board.count_o_on_board()==3 and board.count_x_on_board()==3 \
                    else self.database_4_3 if board.count_o_on_board()==3 and board.count_x_on_board()==4 \
                    else self.database_4_3 if board.count_o_on_board()==4 and board.count_x_on_board()==3 \
                    else self.database_4_4 )

        result = database.get_best_move(board)
        if result is not None:
            # Position is already in the database
            (k_start, k_end, k_removal, outcome, calculated_depth) = result
            if self.verbose:
                print(f'Move is in database already :)  (outcome {outcome}, depth {calculated_depth})')
            if outcome==0 and calculated_depth<self.max_depth:
                if self.verbose:
                    print(f'...but its a tie and depth is only {calculated_depth}, doing minmax anyway to depth {self.max_depth}...')
                k_start, k_end, k_removal, outcome, calculated_depth = self.min_max_best_move(board, 0, -float('inf'), float('inf'), board.xmove)
                    
        else:
            if self.verbose:
                print(f'Move is not in database, doing minmax...')
            # Position is not in the database, solve it with min max + alpha-beta
            k_start, k_end, k_removal, outcome, calculated_depth = self.min_max_best_move(board, 0, -float('inf'), float('inf'), board.xmove)
        return (k_start, k_end, k_removal, outcome, calculated_depth)
            
    def min_max_best_move(self, board: Board_With_History, depth: int, alpha: float, beta: float, maximizing_player: bool) -> tuple[int, int, int, int, int]:
        k_best_start = k_best_end = k_best_removal = k_calculated_depth = -1
        best_outcome = -float('inf') if maximizing_player else float('inf')
        broken = False

        # Check for terminal states
        winner = board.check_winner()
        if winner == 1:  # X wins
            return -1, -1, -1, 100, 0
        elif winner == -1:  # O wins
            return -1, -1, -1, -100, 0
        if board.check_for_repetition():
            return -1, -1, -1, 0, 0  # Draw due to repetition
        if depth >= self.max_depth:
            return -1, -1, -1, 0, 0  # Draw due to depth limit
        
        database = (self.database_3_3 if board.count_o_on_board()==3 and board.count_x_on_board()==3 \
                    else self.database_4_3 if board.count_o_on_board()==3 and board.count_x_on_board()==4 \
                    else self.database_4_3 if board.count_o_on_board()==4 and board.count_x_on_board()==3 \
                    else self.database_4_4 )
        
        # Check if board is in the database
        result = database.get_best_move(board)
        if result is not None:
            # Position is already in the database
            (k_start, k_end, k_removal, outcome, calclated_depth) = result
            # Don't recalculate unless the stored result is a draw at lower depth than we currently calculate.
            if outcome!=0 or calclated_depth>=self.max_depth-depth:
                return k_start, k_end, k_removal, outcome, calclated_depth

        # Iterate over possible moves
        for (i, j) in board.get_xs() if maximizing_player else board.get_os():
            for (ii, jj) in board.get_possible_moves(i, j):
                board_moved = Board_With_History(board)
                if maximizing_player:
                    board_moved.move_x(i, j, ii, jj)
                    board_moved.xmove = False
                else:
                    board_moved.move_o(i, j, ii, jj)
                    board_moved.xmove = True

                if board_moved.is_in_mill(ii, jj):
                    for (iii, jjj) in board_moved.get_os() if maximizing_player else board_moved.get_xs():
                        if board_moved.o_out_of_mill() and board_moved.is_in_mill(iii, jjj):
                            continue
                        board_removed = Board_With_History(board_moved)
                        if maximizing_player:
                            board_removed.remove_o(iii, jjj)
                        else:
                            board_removed.remove_x(iii, jjj)

                        _, _, _, outcome, calc_depth = self.min_max_best_move(board_removed, depth + 1, alpha, beta, not maximizing_player)

                        if maximizing_player:
                            if outcome > best_outcome:
                                best_outcome = outcome
                                k_best_start = i * 8 + j
                                k_best_end = ii * 8 + jj
                                k_best_removal = iii * 8 + jjj
                                k_calculated_depth = calc_depth
                            alpha = max(alpha, best_outcome)
                            # There's not going to be a better move than this!
                            if outcome==99:
                                break
                        else:
                            if outcome < best_outcome:
                                best_outcome = outcome
                                k_best_start = i * 8 + j
                                k_best_end = ii * 8 + jj
                                k_best_removal = iii * 8 + jjj
                                k_calculated_depth = calc_depth
                            beta = min(beta, best_outcome)
                            # There's not going to be a better move than this!
                            if outcome==-98:
                                break

                        if beta <= alpha and self.prune:
                            broken = True
                            break
                else:

                    _, _, _, outcome, calc_depth = self.min_max_best_move(board_moved, depth + 1, alpha, beta, not maximizing_player)

                    if maximizing_player:
                        if outcome > best_outcome:
                            best_outcome = outcome
                            k_best_start = i * 8 + j
                            k_best_end = ii * 8 + jj
                            k_best_removal = -1
                            k_calculated_depth = calc_depth
                        alpha = max(alpha, best_outcome)
                    else:
                        if outcome < best_outcome:
                            best_outcome = outcome
                            k_best_start = i * 8 + j
                            k_best_end = ii * 8 + jj
                            k_best_removal = -1
                            k_calculated_depth = calc_depth
                        beta = min(beta, best_outcome)
                    if beta <= alpha and self.prune:
                        broken = True
                        break
            if beta <= alpha and self.prune:
                broken = True
                break

        new_outcome  = best_outcome - 1 if best_outcome>0 else best_outcome + 1 if best_outcome<0 else 0
        k_calculated_depth += 1

        if not broken:
            # Saves this position to the database
            if result is None:
                database.add_best_move(board, k_best_start, k_best_end, k_best_removal, new_outcome, k_calculated_depth)
            # Updates the position database if the entry already exists
            else:
                database.update_best_move(board, k_best_start, k_best_end, k_best_removal, new_outcome, k_calculated_depth)

        return k_best_start, k_best_end, k_best_removal, new_outcome, k_calculated_depth
        
    def get_removal(self, board: Board_With_History) -> list[int, int]:
        """Remove the piece as stored."""
        return (self.k_removal//8, self.k_removal%8)

    def end_game(self, outcome: int) -> None:
        if self.close_on_end:
            self.clean_up()

    def clean_up(self) -> None:
        self.database_3_3.close()
        self.database_4_3.close()
        self.database_4_4.close()