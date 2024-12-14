from board_visual import Board_Visual
from game_visual import Game_Visual
from game import Game
from player import Player
from player_human import Human
from player_random import Player_Random
from player_alphabeta import Player_AlphaBeta
from random import sample
from rotator import Rotator
import sys

if __name__ == "__main__":
    n_games = int(sys.argv[1]) if len(sys.argv)>=2 else 10
    visual = bool(sys.argv[2]) if len(sys.argv)>=3 else False
    depth = int(sys.argv[3]) if len(sys.argv)==4 else 9
    p1 = Player_AlphaBeta("alphabeta_p1")
    p2 = Player_AlphaBeta("alphabeta_p2")
    p1.verbose = True
    p2.verbose = True
    p2.isX = False
    p1.isX = True
    p1.prune = False
    p2.prune = False
    p1.max_depth = depth
    p2.max_depth = depth
    p1.close_on_end = False
    p2.close_on_end = False

    for i_game in range(n_games):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        game = Game_Visual(p1,p2) if visual else Game(p1,p2)
        game.verbose = True
        game.board.xinhand = 0
        game.board.oinhand = 0

        pieces = sample(range(24),7)
        for i in range(4):
            game.board.flip_x_at_k(pieces[i])
        for i in range(3):
            game.board.flip_o_at_k(pieces[i+4])
        if visual:
            game.board.save_state_to_history()
        
        game.game_loop()
        if visual:
            game.replay_game()

    p1.clean_up()
    p2.clean_up()