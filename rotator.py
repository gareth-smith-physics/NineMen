import numpy as np
from board import Board

class Rotator:
    def __init__(self) -> None:
        self.r1 = self.generate_rotation_matrix()
        self.r2 = self.generate_flip_matrix()
        self.r3 = self.generate_inversion_matrix()
        self.i1 = self.combine_rotation_matricies([self.r1,self.r1,self.r1])
        self.i2 = self.r2
        self.i3 = self.r3
        self.rotation_list = self.generate_rotation_list()
        self.inverse_rotation_list = self.generate_inverse_rotation_list()
        self.index_rotation_list = self.generate_index_rotation_list()
        self.inverse_index_rotation_list = self.generate_inverse_index_rotation_list()
    
    def generate_rotation_matrix(self) -> np.ndarray[int]:
        """Generate the rotation matrix."""
        rotation_matrix = np.zeros((24,24),dtype=int)
        for i in range(3):
            for j in range(8):
                k = i*8 + j
                k2 = i*8 + ((j+2)%8)
                rotation_matrix[k][k2] = 1
        return rotation_matrix
    
    def generate_flip_matrix(self) -> np.ndarray[int]:
        """Generate the flip matrix."""
        rotation_matrix = np.zeros((24,24),dtype=int)
        jflip = (2,1,0,7,6,5,4,3)
        for i in range(3):
            for j in range(8):
                k = i*8 + j
                j2 = jflip[j]
                k2 = i*8 + j2
                rotation_matrix[k][k2] = 1
        return rotation_matrix
    
    def generate_inversion_matrix(self) -> np.ndarray[int]:
        """Generate the inversion matrix."""
        rotation_matrix = np.zeros((24,24),dtype=int)
        for i in range(3):
            for j in range(8):
                k = i*8 + j
                i2 = 2-i
                k2 = i2*8 + j
                rotation_matrix[k][k2] = 1
        return rotation_matrix
    
    def combine_rotation_matricies(self, rotations: list[np.ndarray[int]]) -> np.ndarray[int]:
        """Combine multiple rotation matrices into one."""
        mat = np.identity(24)
        for rotation in reversed(rotations):
            mat = np.matmul(rotation,mat)
        return mat

    def generate_rotation_list(self) -> list[np.ndarray[int]]:
        """Generates a list of all the unique rotation matrices."""
        rots = [[],
                [self.r1],
                [self.r1,self.r1],
                [self.r1,self.r1,self.r1],
                [self.r2],
                [self.r1,self.r2],
                [self.r1,self.r1,self.r2],
                [self.r1,self.r1,self.r1,self.r2],
                [self.r3],
                [self.r1,self.r3],
                [self.r1,self.r1,self.r3],
                [self.r1,self.r1,self.r1,self.r3],
                [self.r2,self.r3],
                [self.r1,self.r2,self.r3],
                [self.r1,self.r1,self.r2,self.r3],
                [self.r1,self.r1,self.r1,self.r2,self.r3]]
        return [self.combine_rotation_matricies(rotation_list) for rotation_list in rots]
    
    def generate_inverse_rotation_list(self) -> list[np.ndarray[int]]:
        """Generates a list of the inverses of all the unique rotation matrices."""
        rots = [[],
                [self.i1],
                [self.i1,self.i1],
                [self.i1,self.i1,self.i1],
                [self.i2],
                [self.i2,self.i1],
                [self.i2,self.i1,self.i1],
                [self.i2,self.i1,self.i1,self.i1],
                [self.i3],
                [self.i3,self.i1],
                [self.i3,self.i1,self.i1],
                [self.i3,self.i1,self.i1,self.i1],
                [self.i3,self.i2],
                [self.i3,self.i2,self.i1],
                [self.i3,self.i2,self.i1,self.i1],
                [self.i3,self.i2,self.i1,self.i1,self.i1]]
        return [self.combine_rotation_matricies(rotation_list) for rotation_list in rots]
    
    def apply_rotation(self, board: Board, rotation: np.ndarray[int]) -> Board:
        """Apply a single arbitrary rotation."""
        x = board.get_x_array()
        o = board.get_o_array()
        x = np.matmul(rotation,x)
        o = np.matmul(rotation,o)
        board.set_x_from_array(x)
        board.set_o_from_array(o)
        return board
    
    def apply_rotation_by_index(self, board: Board, index: int):
        """Apply a single rotation from the rotation list."""
        if index<0 or index>=len(self.rotation_list):
            return board
        x = board.get_x_array()
        o = board.get_o_array()
        x = np.matmul(self.rotation_list[index],x)
        o = np.matmul(self.rotation_list[index],o)
        board.set_x_from_array(x)
        board.set_o_from_array(o)
        return board
    
    def apply_inverse_rotation_by_index(self, board: Board, index: int):
        """Apply an inverse rotation from the rotation list."""
        if index<0 or index>=len(self.inverse_rotation_list):
            return board
        x = board.get_x_array()
        o = board.get_o_array()
        x = np.matmul(self.inverse_rotation_list[index],x)
        o = np.matmul(self.inverse_rotation_list[index],o)
        board.set_x_from_array(x)
        board.set_o_from_array(o)
        return board
    
    def is_rotation(self, board_1: Board, board_2: Board) -> int:
        """Check if board1 is a rotation of board2. Return -1 if not, otherwise 
        return the rotation index to get from board 2 to board 1."""
        board1 = Board(board_1)
        board2 = Board(board_2)
        if board1.xinhand != board2.xinhand or board1.oinhand != board2.oinhand:
            return -1
        if board1.x.bit_count() != board2.x.bit_count() or board1.o.bit_count()  != board2.o.bit_count():
            return -1
        x1 = board1.get_x_array()
        o1 = board1.get_o_array()
        x2 = board2.get_x_array()
        o2 = board2.get_o_array()
        for i in range(len(self.rotation_list)):
            r = self.rotation_list[i]
            x2p = np.matmul(r,x2)
            o2p = np.matmul(r,o2)
            if x1==x2p and o1==o2p:
                return i
        return -1
    
    def swap_x_and_o(self, board: Board) -> Board:
        """Swap X and O."""
        u = board.x
        board.x = board.o
        board.o = u
        j = board.xinhand
        board.xinhand = board.oinhand
        board.oinhand = j
        board.xmove = not board.xmove
        return board

    def get_equivalence_board(self, board: Board) -> tuple[Board,int]:
        """Returns a representative board for the equivalence class of all boards
        that are rotations of a given board. Swaps so it is X to move."""
        board2 = Board(board)
        if not board2.xmove:
            self.swap_x_and_o(board2)
        min_x = board2.x
        best_i = 0
        for i in range(len(self.rotation_list)):
            board3 = Board(board2)
            board3 = self.apply_rotation_by_index(board3, i)
            if board3.x < min_x:
                min_x = board3.x
                best_i = i
        self.apply_rotation_by_index(board2,best_i)
        return board2, best_i

    def generate_index_rotation(self, rotation: np.ndarray[int]) -> list[int]:
        """Generate a list of new cell indices after a given rotation."""
        rotated_ks = []
        for k in range(24):
            board = Board()
            board.flip_x_at_k(k)
            self.apply_rotation(board,rotation)
            for pk in range(24):
                if board.is_x_at_k(pk):
                    rotated_ks.append(pk)
                    break
        return rotated_ks
    
    def generate_index_rotation_list(self) -> list[list[int]]:
        """Generate the new indices after each rotation in the rotation list."""
        return [self.generate_index_rotation(rotation) for rotation in self.rotation_list]
    
    def generate_inverse_index_rotation_list(self) -> list[list[int]]:
        """Generate the new indices after each rotation in the inverse rotation list."""
        return [self.generate_index_rotation(rotation) for rotation in self.inverse_rotation_list]
    
    