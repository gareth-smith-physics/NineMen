from board import Board

class Player:
    def __init__(self) -> None:
        self.name = "player"
        self.gui = False
        self.isX = False
        self.verbose = False

    # Placeholder for get placement, [i, j]
    def get_placement(self, board: Board) -> list[int,int]:
        return [0,0]
    
    # Placeholder for get move, [i, j, ii, jj]
    def get_move(self, board: Board) -> list[int,int,int,int]:
        return [0,0,0,0]
    
    # Placeholder for get removal, [i, j]
    def get_removal(self, board: Board) -> list[int,int]:
        return [0,0]

    # Placeholder for end game
    def end_game(self, outcome: int) -> None:
        pass
