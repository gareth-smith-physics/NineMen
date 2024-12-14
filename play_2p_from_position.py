from board_visual import Board_Visual
from game_visual import Game_Visual
from player import Player
from player_human import Human
from player_random import Player_Random
from player_alphabeta import Player_AlphaBeta
from random import sample

if __name__ == "__main__":
    p1 = Human("p1")
    p2 = Human("p2")
    p1.verbose = True
    p2.verbose = True
    p2.isX = False
    p1.isX = True
    game = Game_Visual(p1,p2)
    game.verbose = True
    game.board.xinhand = 0
    game.board.oinhand = 0

    pieces = sample(range(24),6)
    for i in range(3):
        game.board.flip_x_at_k(pieces[i])
    for i in range(3):
        game.board.flip_o_at_k(pieces[i+3])
    """
    game.board.flip_x(2,0)
    game.board.flip_x(1,4)
    game.board.flip_x(1,7)
    game.board.flip_o(0,0)
    game.board.flip_o(0,1)
    game.board.flip_o(0,3)
    """
    
    game.game_loop()