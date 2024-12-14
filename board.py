import numpy as np

class Board:
    def __init__(self, b = None) -> None:
        if b is None:
            self.x = 0              # Bitboard for X pieces
            self.o = 0              # Bitboard for X pieces
            self.xinhand = 9        # Number of unplayed X pieces
            self.oinhand = 9        # Number of unplayed O pieces
            self.xmove = True       # X to move?
        else:
            self.x = b.x               # Bitboard for X pieces
            self.o = b.o               # Bitboard for X pieces
            self.xinhand = b.xinhand   # Number of unplayed X pieces
            self.oinhand = b.oinhand  # Number of unplayed O pieces
            self.xmove = b.xmove      # X to move?

    def tile_state(self, i: int, j: int) -> str:
        """Get the state of a tile ('X', 'O', or empty)."""
        if self.is_x(i,j):
            return "X"
        elif self.is_o(i,j):
            return "O"
        return " "
    
    def is_connected(self, i1, j1, i2, j2) -> bool:
        """Check if two points should be connected by a line (simple connection rules)."""
        # Define connections based on the Nine Men's Morris board rules
        if i1==i2:
            if (j1-j2)%8 in (1,7):
                return True
        else:
            if j1==j2 and j1%2==1 and (i1==1 or i2==1):
                return True
        return False

    def is_empty(self, i: int, j: int) -> bool:
        """Check if a tile is empty."""
        return not (self.is_x(i,j) or self.is_o(i,j))
    
    def is_x_at_k(self, k: int) -> bool:
        """Check if a cell contains an X piece."""
        return (self.x >> k) & 1 

    def is_o_at_k(self, k: int) -> bool:
        """Check if a cell contains an O piece."""
        return (self.o >> k) & 1
    
    def is_x(self, i: int, j: int) -> bool:
        """Check if a cell contains an X piece."""
        return (self.x >> i*8+j) & 1 

    def is_o(self, i: int, j: int) -> bool:
        """Check if a cell contains an O piece."""
        return (self.o >> i*8+j) & 1
    
    def flip_x(self, i: int, j: int) -> None:
        """Either add or remove an X piece from a cell."""
        self.x ^= (1 << i*8+j)
            
    def flip_o(self, i: int, j: int) -> None:
        """Either add or remove an O piece from a cell."""
        self.o ^= (1 << i*8+j)

    def flip_x_at_k(self, k: int) -> None:
        """Either add or remove an X piece from a cell."""
        self.x ^= (1 << k)
            
    def flip_o_at_k(self, k: int) -> None:
        """Either add or remove an O piece from a cell."""
        self.o ^= (1 << k)

    def add_x(self, i:int, j:int) -> None:
        """Add a X piece at a positon, and remove one from the hand."""
        self.flip_x(i,j)
        self.xinhand -= 1

    def add_x_at_k(self, k:int) -> None:
        """Add a X piece at a positon, and remove one from the hand."""
        self.flip_x_at_k(k)
        self.xinhand -= 1

    def add_o(self, i:int, j:int) -> None:
        """Add an O piece at a positon, and remove one from the hand."""
        self.flip_o(i,j)
        self.oinhand -= 1

    def add_o_at_k(self, k:int) -> None:
        """Add an O piece at a positon, and remove one from the hand."""
        self.flip_o_at_k(k)
        self.oinhand -= 1

    def move_x(self, i:int, j:int, ii:int, jj:int) -> None:
        """Move an X piece from one position to another."""
        self.flip_x(i,j)
        self.flip_x(ii,jj)

    def move_x_by_k(self, k:int, kk:int) -> None:
        """Move an X piece from one position to another."""
        self.flip_x_at_k(k)
        self.flip_x_at_k(kk)

    def move_o(self, i:int, j:int, ii:int, jj:int) -> None:
        """Move an O piece from one position to another."""
        self.flip_o(i,j)
        self.flip_o(ii,jj)

    def move_o_by_k(self, k:int, kk:int) -> None:
        """Move an O piece from one position to another."""
        self.flip_o_at_k(k)
        self.flip_o_at_k(kk)

    def remove_x(self, i:int, j:int) -> None:
        """Remove an X piece."""
        self.flip_x(i,j)

    def remove_x_by_k(self, k:int) -> None:
        """Move an X piece."""
        self.flip_x_at_k(k)

    def remove_o(self, i:int, j:int) -> None:
        """Remove an O piece."""
        self.flip_o(i,j)

    def remove_o_by_k(self, k:int) -> None:
        """Remove an O piece."""
        self.flip_o_at_k(k)

    def print_board(self) -> None:
        """Print the board."""
        print()
        print(f'{self.tile_state(0,0)} - - - - - {self.tile_state(0,1)} - - - - - {self.tile_state(0,2)}')
        print(f'|           |           |')
        print(f'|   {self.tile_state(1,0)} - - - {self.tile_state(1,1)} - - - {self.tile_state(1,2)}   |')
        print(f'|   |       |       |   |')
        print(f'|   |   {self.tile_state(2,0)} - {self.tile_state(2,1)} - {self.tile_state(2,2)}   |   |')
        print(f'|   |   |       |   |   |')
        print(f'{self.tile_state(0,7)} - {self.tile_state(1,7)} - {self.tile_state(2,7)}       {self.tile_state(2,3)} - {self.tile_state(1,3)} - {self.tile_state(0,3)}')
        print(f'|   |   |       |   |   |')
        print(f'|   |   {self.tile_state(2,6)} - {self.tile_state(2,5)} - {self.tile_state(2,4)}   |   |')
        print(f'|   |       |       |   |')
        print(f'|   {self.tile_state(1,6)} - - - {self.tile_state(1,5)} - - - {self.tile_state(1,4)}   |')
        print(f'|           |           |')
        print(f'{self.tile_state(0,6)} - - - - - {self.tile_state(0,5)} - - - - - {self.tile_state(0,4)}')
        print()

    def is_in_mill(self, i: int, j: int) -> bool:
        """Check if a piece at position (i, j) is part of a mill."""
        # Determine whose piece is at (i, j)
        getter = self.is_x if self.is_x(i,j) else self.is_o if self.is_o(i,j) else None
        if getter is None:
            return False  # No piece here, so it can't be in a mill.

        # Horizontal mills: Define valid patterns per ring
        horizontal_patterns = [
            (0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 0)
        ]
        horizontal_mill = any(
            all(getter(i, col) for col in pattern) for pattern in horizontal_patterns if j in pattern
        )

        # Vertical mills: Check same position across rings (only for even indices)
        vertical_mill = (
            j % 2 == 1 and 
            getter((i - 1) % 3, j) and getter((i + 1) % 3, j)
        )

        return horizontal_mill or vertical_mill
    
    def get_mills(self, getter) -> list[tuple[int,int,int,int]]:
        """Return a list of the mills"""
        mills = []
        # Horizontal mills: Define valid patterns per ring
        horizontal_patterns = [
            (0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 0)
        ]
        for i in range(3):
            for pattern in horizontal_patterns:
                if all(getter(i,j) for j in pattern):
                    mills.append((i,pattern[0],i,pattern[2]))

        # Vertical mills: Check same position across rings (only for even indices)
        for j in range(8):
            if j % 2 ==1:
                if all(getter(i,j) for i in range(3)):
                    mills.append((0,j,2,j))

        return mills

    def get_x_mills(self) -> list[tuple[int,int,int,int]]:
        return self.get_mills(self.is_x)

    def get_o_mills(self) -> list[tuple[int,int,int,int]]:
        return self.get_mills(self.is_o)


    def x_out_of_mill(self) -> bool:
        """Check if X has any rocks out of a mill."""
        return any(self.is_x(i,j) and not self.is_in_mill(i, j) for i in range(3) for j in range(8))

    def o_out_of_mill(self) -> bool:
        """Check if O has any rocks out of a mill."""
        return any(self.is_o(i,j) and not self.is_in_mill(i, j) for i in range(3) for j in range(8))

    def rock_has_move(self, i: int, j: int) -> bool:
        """Check if a rock can move."""
        return any([
            self.is_empty(i, (j + 1) % 8),
            self.is_empty(i, (j - 1) % 8),
            i < 2 and self.is_empty(i + 1, j) and j%2==1,
            i > 0 and self.is_empty(i - 1, j) and j%2==1
        ])

    def x_has_move(self) -> bool:
        """Check if X has any valid moves."""
        xs = self.get_xs()
        if len(xs)==3:
            return True
        for (i,j) in xs:
            if self.rock_has_move(i,j):
                return True
        return False

    def o_has_move(self) -> bool:
        """Check if O has any valid moves."""
        os = self.get_os()
        if len(os)==3:
            return True
        for (i,j) in os:
            if self.rock_has_move(i,j):
                return True
        return False

    def get_empty_tiles(self) -> list[tuple[int,int]]:
        """Get a list of all the empty tiles."""
        empties = []
        for i in range(3):
            for j in range(8):
                if self.is_empty(i,j):
                    empties.append((i,j))
        return empties

    def get_possible_moves(self, i: int, j: int) -> list[tuple[int,int]]:
        """Get a list of the tiles a piece can move to."""
        if self.is_empty(i,j):
            return []
        flying = (self.count_x_on_board()==3) if self.is_x(i,j) else (self.count_o_on_board()==3) if self.is_o(i,j) else False
        moves = []
        for ii in range(3):
            for jj in range(8):
                if ((self.is_empty(ii,jj)) if flying else (self.is_empty(ii,jj) and self.is_connected(i,j,ii,jj))):
                    moves.append((ii,jj))
        return moves

    def get_xs(self) -> list[tuple[int,int]]:
        """Get a list of the positions of all the X pieces."""
        xs = []
        for i in range(3):
            for j in range(8):
                if self.is_x(i,j):
                    xs.append((i,j))
        return xs

    def get_os(self) -> list[tuple[int,int]]:
        """Get a list of the positions of all the O pieces."""
        os = []
        for i in range(3):
            for j in range(8):
                if self.is_o(i,j):
                    os.append((i,j))
        return os

    def count_x_on_board(self) -> int:
        """Count the number of X pieces on the board."""
        return self.x.bit_count()

    def count_o_on_board(self) -> int:
        """Count the number of O pieces on the board."""
        return self.o.bit_count()

    def get_x_array(self) -> np.ndarray:
        """Return the X bitboard as an array of bools."""
        return np.array([(self.x >> k) & 1 for k in range(24)])
    
    def get_o_array(self) -> np.ndarray:
        """Return the O bitboard as an array of bools."""
        return np.array([(self.o >> k) & 1 for k in range(24)])
    
    def set_x_from_array(self, x_array: np.ndarray) -> None:
        """Set the X bitboard to something new given by an array of bools."""
        out = 0
        for bit in reversed(x_array):
            out = (out << 1) | int(bit)
        self.x = out

    def set_o_from_array(self, o_array: np.ndarray) -> None:
        """Set the O bitboard to something new given by an array of bools."""
        out = 0
        for bit in reversed(o_array):
            out = (out << 1) | int(bit)
        self.o = out

    def check_winner(self) -> int:
        """Check if the game is over and declare the winner."""
        if self.xinhand == 0 and (not self.x_has_move() or self.count_x_on_board() < 3):
            return -1
        if self.oinhand == 0 and (not self.o_has_move() or self.count_o_on_board() < 3):
            return 1
        return 0

