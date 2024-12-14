from board_with_history import Board_With_History
from player_alphabeta import Player_AlphaBeta
from rotator import Rotator
from itertools import combinations
import sys

print_every = 171

if __name__ == "__main__":
    i = 0
    p1 = Player_AlphaBeta("alphabeta_p1")
    p1.prune = False
    for depth in [12,16,22]:
    #for depth in [4,6,8]:
        p1.max_depth = depth
        for c in combinations(range(24),7):
            for cx in combinations(c,4):
                board = Board_With_History()
                board.xinhand = 0
                board.oinhand = 0
                co = [p for p in c if p not in cx]
                for x in cx:
                    board.flip_x_at_k(x)
                for o in co:
                    board.flip_o_at_k(o)
                board.save_state_to_history()
                if i%print_every==0:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(f'Running board {i}')
                    board.print_board()
                    p1.verbose = True
                k1, k2, k3, outcome, calculated_depth = p1.calculate_best_move(board)
                if i%print_every==0:
                    board.move_x_by_k(k1,k2)
                    board.print_board()
                    print(f'Outcome: {outcome}, depth: {calculated_depth}')
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                    p1.verbose = False
                i += 1
            for cx in combinations(c,3):
                board = Board_With_History()
                board.xinhand = 0
                board.oinhand = 0
                co = [p for p in c if p not in cx]
                for x in cx:
                    board.flip_x_at_k(x)
                for o in co:
                    board.flip_o_at_k(o)
                board.save_state_to_history()
                if i%print_every==0:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(f'Running board {i}')
                    board.print_board()
                    p1.verbose = True
                k1, k2, k3, outcome, calculated_depth = p1.calculate_best_move(board)
                if i%print_every==0:
                    board.move_x_by_k(k1,k2)
                    board.print_board()
                    print(f'Outcome: {outcome}, depth: {calculated_depth}')
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                    p1.verbose = False
                i += 1