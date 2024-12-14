from board_visual import Board_Visual
from board_with_history import Board_With_History
from game_visual import Game_Visual
from player import Player
from player_human import Human
from player_random import Player_Random
from player_alphabeta import Player_AlphaBeta
from random import sample

if __name__ == "__main__":
    p1 = Human("human",True)
    #p2 = Human("p2",True)
    p2 = Player_AlphaBeta("alphabeta")
    p1.verbose = True
    p2.verbose = True
    p2.isX = False
    p1.isX = True
    game = Game_Visual(p1,p2)
    game.verbose = True
    game.board.xinhand = 0
    game.board.oinhand = 0
    p2.max_depth = 9
    p2.prune = False
    
    pieces = sample(range(24),7)
    for i in range(4):
        game.board.flip_o_at_k(pieces[i])
    for i in range(3):
        game.board.flip_x_at_k(pieces[i+4])
    game.board.save_state_to_history()
    
    game.game_loop()
    game.replay_game()