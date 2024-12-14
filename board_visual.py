import pygame
import numpy as np
from board import Board  # Assuming Board is your original class

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_COLOR = (255, 0, 0)  # Red for X
O_COLOR = (0, 0, 255)  # Blue for O
X_MILL_COLOR = (255, 100, 100)  # Red for X
O_MILL_COLOR = (100, 100, 255)  # Blue for O
HIGHLIGHT_COLOR = (0, 255, 0)  # Green for highlights
LAST_MOVE_COLOR = (200, 200, 0)  # Color for last move
REPLAY_COLOR = (200, 200, 200)  # Color for the background during replays

# Board_Visual class
class Board_Visual(Board):
    def __init__(self, b = None):
        super().__init__(b)
        if b is None:
            self.size = 600  # Total board size
            self.piece_size = 12
            self.center = self.size // 2  # Center of the board
            self.radius = self.size // 3  # Radius for outer points
            # Initialize pygame
            pygame.init()
            self.screen = pygame.display.set_mode((self.size, self.size))
            pygame.display.set_caption("Nine Men's Morris")
            # Points layout for Nine Men's Morris (24 points)
            self.points = self.get_points()
            self.highlight = [-1,-1]
            self.last_move = [-1,-1]
            self.last_move_from = [-1,-1]
            self.last_removed = [-1,-1]
        else:
            self.size = b.size  # Total board size
            self.piece_size = b.piece_size
            self.center = b.center  # Center of the board
            self.radius = b.radius  # Radius for outer points
            # Initialize pygame
            pygame.init()
            self.screen = pygame.display.set_mode((self.size, self.size))
            pygame.display.set_caption("Nine Men's Morris")
            # Points layout for Nine Men's Morris (24 points)
            self.points = b.points
            self.highlight = b.highlight
            self.last_move = b.last_move
            self.last_move_from = b.last_move_from
            self.last_removed = b.last_removed
        

    def get_points(self):
        """Calculate the 24 points on the board based on concentric circles."""
        # Outer square points
        outer = [
            (self.center - self.radius, self.center - self.radius), # Top-left
            (self.center, self.center - self.radius),              # Top-center
            (self.center + self.radius, self.center - self.radius), # Top-right
            (self.center + self.radius, self.center),              # Right-center
            (self.center + self.radius, self.center + self.radius), # Bottom-right
            (self.center, self.center + self.radius),              # Bottom-center
            (self.center - self.radius, self.center + self.radius), # Bottom-left
            (self.center - self.radius, self.center)               # Left-center
        ]
        
        # Middle square points
        middle = [
            (self.center - self.radius * 2 // 3, self.center - self.radius * 2 // 3), # Top-left
            (self.center, self.center - self.radius  * 2 // 3),                     # Top-center
            (self.center + self.radius  * 2 // 3, self.center - self.radius  * 2 // 3), # Top-right
            (self.center + self.radius  * 2 // 3, self.center),                     # Right-center
            (self.center + self.radius  * 2 // 3, self.center + self.radius  * 2 // 3), # Bottom-right
            (self.center, self.center + self.radius  * 2 // 3),                     # Bottom-center
            (self.center - self.radius  * 2 // 3, self.center + self.radius  * 2 // 3), # Bottom-left
            (self.center - self.radius  * 2 // 3, self.center)                      # Left-center
        ]
        
        # Inner square points
        inner = [
            (self.center - self.radius // 3, self.center - self.radius // 3), # Top-left
            (self.center, self.center - self.radius // 3),                     # Top-center
            (self.center + self.radius // 3, self.center - self.radius // 3), # Top-right
            (self.center + self.radius // 3, self.center),                     # Right-center
            (self.center + self.radius // 3, self.center + self.radius // 3), # Bottom-right
            (self.center, self.center + self.radius // 3),                     # Bottom-center
            (self.center - self.radius // 3, self.center + self.radius // 3), # Bottom-left
            (self.center - self.radius // 3, self.center)                      # Left-center
        ]

        # Combine points into a list
        return [outer, middle, inner]

    def draw(self, replay:bool = False) -> None:
        """Draw the Nine Men's Morris board with pieces."""
        self.screen.fill((255, 255, 255))  # Background color (white)

        # Draw the background
        self.draw_background(replay)

        # Draw the lines of the Nine Men's Morris board
        self.draw_lines()

        # Draw the positions (circles) for the pieces
        self.draw_positions()

        # Draws the mill highlighting
        self.draw_mills()

        # Draw the highlight square
        self.draw_highlighted_piece()

        # Draw the last move highlight square
        self.draw_last_move()

        # Draw the pieces (X and O)
        self.draw_pieces()

        # Draws the unplaced pieces
        self.draw_unplaced()

        pygame.display.update()  # Update the screen

    def draw_lines(self) -> None:
        """Draw the lines between points."""
        line_color = (0, 0, 0)  # Black lines
        points = self.points

        # Draw lines connecting points
        for i1 in range(3):
            for i2 in range(3):
                for j1 in range(8):
                    for j2 in range(8):
                        if self.is_connected(i1,j1,i2,j2):
                            pygame.draw.line(self.screen, line_color, points[i1][j1], points[i2][j2], 2)

    def draw_background(self, replay:bool) -> None:
        """Draw the background."""
        if replay:
            pygame.draw.rect(self.screen, REPLAY_COLOR, (0,0,600,600))

    def draw_positions(self) -> None:
        """Draw circles for each position on the board."""
        circle_color = (0, 0, 0)  # Black for the positions
        radius = 6  # Circle radius for positions
        for i in range(3):
            for j in range(8):
                point = self.points[i][j]
                pygame.draw.circle(self.screen, circle_color, point, radius)

    def draw_piece(self,i,j,player) -> None:
        """Draws a piece on the board."""
        color = X_COLOR if player == 0 else O_COLOR
        point = self.points[i][j]
        pygame.draw.circle(self.screen, color, point, self.piece_size)

    def draw_unplaced(self) -> None:
        """Draws the unplaced pieces below the board."""
        x0 = (self.center-self.radius) // 2
        y0 = (self.center+self.radius+self.size) // 2  - self.piece_size
        for k in range(self.xinhand):
            pygame.draw.circle(self.screen, X_COLOR, (x0+3*self.piece_size*k, y0), self.piece_size)
        x0 = (self.center+self.radius+self.size) // 2
        y0 = (self.center+self.radius+self.size) // 2 + 2*self.piece_size
        for k in range(self.oinhand):
            pygame.draw.circle(self.screen, O_COLOR, (x0-3*self.piece_size*k, y0), self.piece_size)

    def draw_highlighted_piece(self) -> None:
        """Draws a square to show the currently highlighted piece."""
        color = HIGHLIGHT_COLOR
        i = self.highlight[0]
        j = self.highlight[1]
        if i==-1 or j==-1:
            return
        point = self.points[i][j]
        rect = (point[0]-1.5*self.piece_size,point[1]-1.5*self.piece_size,3*self.piece_size,3*self.piece_size)
        pygame.draw.rect(self.screen, color, rect)

    def draw_last_move(self) -> None:
        """Draws a square to show the last move."""
        color = LAST_MOVE_COLOR
        i = self.last_move[0]
        j = self.last_move[1]
        if i!=-1 and j!=-1:
            point = self.points[i][j]
            rect = (point[0]-1.5*self.piece_size,point[1]-1.5*self.piece_size,3*self.piece_size,3*self.piece_size)
            pygame.draw.rect(self.screen, color, rect)
        i = self.last_move_from[0]
        j = self.last_move_from[1]
        if i!=-1 and j!=-1:
            point = self.points[i][j]
            rect = (point[0]-1.5*self.piece_size,point[1]-1.5*self.piece_size,3*self.piece_size,3*self.piece_size)
            pygame.draw.rect(self.screen, color, rect)
        i = self.last_removed[0]
        j = self.last_removed[1]
        if i!=-1 and j!=-1:
            point = self.points[i][j]
            rect = (point[0]-1.5*self.piece_size,point[1]-1.5*self.piece_size,3*self.piece_size,3*self.piece_size)
            pygame.draw.rect(self.screen, color, rect)

    def highlight_piece(self,i,j) -> None:
        """Highlights a piece."""
        self.highlight[0] = i
        self.highlight[1] = j

    def clear_highlight(self) -> None:
        """Resets the highlighting."""
        self.highlight[0] = -1
        self.highlight[1] = -1

    def draw_pieces(self) -> None:
        """Draw the pieces (X and O)."""
        for i in range(3):
            for j in range(8):
                if self.is_x(i,j):
                    self.draw_piece(i,j,0)
                if self.is_o(i,j):
                    self.draw_piece(i,j,1)

    def draw_mill(self, mill: tuple[int,int,int,int], color: tuple[int,int,int]):
        point1 = self.points[mill[0]][mill[1]]
        point2 = self.points[mill[2]][mill[3]]
        x0 = min((point1[0],point2[0])) - 2*self.piece_size
        y0 = min((point1[1],point2[1])) - 2*self.piece_size
        width = abs(point1[0]-point2[0]) + 4*self.piece_size
        height = abs(point1[1]-point2[1]) + 4*self.piece_size
        pygame.draw.rect(self.screen, color, (x0,y0,width,height))

    def draw_mills(self) -> None:
        """Draw some squares around the mills."""
        for mill in self.get_x_mills():
            self.draw_mill(mill,X_MILL_COLOR)
        for mill in self.get_o_mills():
            self.draw_mill(mill,O_MILL_COLOR)

    def handle_click(self, pos) -> tuple[int, int]:
        """Handles mouse clicks to place or move pieces."""
        x, y = pos
        best_i, best_j = 0,0
        min_dist = 1e9
        for i in range(3):
            for j in range(8):
                point = self.points[i][j]
                dist = np.sqrt((x-point[0])*(x-point[0]) + (y-point[1])*(y-point[1]))
                if dist<min_dist:
                    min_dist = dist
                    best_i = i
                    best_j = j
        return best_i,best_j