from board_visual import Board_Visual
from game_visual import Game_Visual
from player import Player
from player_human import Human
from player_random import Player_Random

if __name__ == "__main__":
    p1 = Human("p1",True)
    #p2 = Human("p2",True)
    p2 = Player_Random("random")
    game = Game_Visual(p1,p2)
    game.verbose = True
    game.game_loop()