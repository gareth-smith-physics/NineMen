import numpy as np
from board import Board
from board_visual_with_history import Board_Visual_With_History
from player import Player
from player_human import Human
from game import Game
import pygame
from rotator import Rotator

class Game_Visual(Game):
    def __init__(self, p1: Player, p2: Player) -> None:
        super().__init__(p1,p2)
        self.board = Board_Visual_With_History()    # The board

    def move(self, i: int, j: int, ii: int, jj: int) -> bool:
        moved = super().move(i,j,ii,jj)
        if moved:
            self.board.last_move = [ii,jj]
            self.board.last_move_from = [i,j]
            self.board.last_removed = [-1,-1]
        return moved
    
    def place(self, i: int, j: int) -> bool:
        moved = super().place(i,j)
        if moved:
            self.board.last_move = [i,j]
            self.board.last_removed = [-1,-1]
        return moved
    
    def remove(self, i: int, j: int) -> bool:
        moved = super().remove(i,j)
        if moved:
            self.board.last_removed = [i,j]
        return moved

    def game_loop(self) -> None:
        """Main game loop."""
        running = True
        i, j, ii, jj = 0, 0, -1, -1
        clicked = False
        while running:
            self.board.draw()
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.tie()
                # Handle mouse clicks to place pieces or remove pieces
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        i, j = self.board.handle_click(pygame.mouse.get_pos())
                        clicked = True

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
            if player.gui and not clicked:
                pygame.time.Clock().tick(30)
                continue
            
            if self.isremove:
                if not player.gui:
                    i, j = player.get_removal(self.board)
                moved = self.remove(i, j)
            elif self.board.xmove and self.board.xinhand > 0 or not self.board.xmove and self.board.oinhand > 0:
                if not player.gui:
                    i, j = player.get_placement(self.board)
                moved = self.place(i, j)
            else:
                if not player.gui:
                    i, j, ii, jj = player.get_move(self.board)
                    moved = self.move(i, j, ii, jj)
                    ii=-1
                    jj=-1
                if player.gui:
                    if ii==-1 and jj==-1:
                        if (self.board.xmove and self.board.is_x(i,j)) or (not self.board.xmove and self.board.is_o(i,j)):
                            ii=i
                            jj=j
                            self.board.highlight_piece(i,j)
                    else:
                        self.board.clear_highlight()
                        moved = self.move(ii, jj, i, j)
                        ii=-1
                        jj=-1
            clicked = False
            if moved:
                self.board.save_state_to_history()

        pygame.display.quit()
        pygame.quit()

    def replay_game(self) -> None:
        """Replay the game with gui."""
        running = True
        move_number = 0
        while running:
            board = self.board.get_board_at_move(move_number)
            if board is None:
                return
            board.draw(replay=True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse clicks to place pieces or remove pieces
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        move_number += 1

            pygame.time.Clock().tick(30)
            
        pygame.display.quit()
        pygame.quit()
