import sqlite3
from board import Board
from rotator import Rotator
from board_visual_with_history import Board_Visual_With_History
from player import Player
from game_visual import Game_Visual

class Database:
    def __init__(self, db_name="positions.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        self.rotator = Rotator()

    def _create_table(self):
        """Creates the positions database if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x INTEGER NOT NULL,
                o INTEGER NOT NULL,
                k_move INTEGER NOT NULL
            )
        ''')
        self.connection.commit()
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx3 ON positions (
                x,
                o
            )
        ''')
        self.connection.commit()

    def intify(self, k_start: int, k_end: int, k_removal: int, outcome: int, depth: int) -> int:
        """Converts the best move (piece to move, square to move to, piece to remove),
        the outcome (100-moves to win, or -100+moves ot lose, or 0=draw),
        and the calculated depth (bug in code, also max depth = 99),
        to a single int for databse storage."""
        return k_start + 100*k_end + 10000*k_removal + 1000000*depth + 100000000*outcome
    
    def deintify(self, num: int) -> tuple[int,int,int,int,int]:
        """Decodes the max depth from the database.
        Added a hack to treat outcome=-1, depth=0 as a draw as well,
        since the database got corrupted by calculating to a depth > 99."""
        pp = 0
        while num<-9000000:
            num += 100000000
            pp += 1
        num += 10000
        k_start = num % 100
        num -= k_start
        k_end = (num % 10000) // 100
        num -= k_end*100
        num -= 10000
        k_removal = ((num+50000) % 1000000) // 10000 - 5
        num -= k_removal*10000
        depth = (num % 100000000) // 1000000
        num -= depth*1000000
        num -= 100000000 * pp
        outcome = num // 100000000
        if (outcome==-1 and depth==0):
            outcome = 0
            depth = 99
        return (int(k_start),int(k_end),int(k_removal),int(outcome),int(depth))

    def add_entry(self, x: int, o: int, k_move: int) -> None:
        """Adds a new entry to the positions database."""
        self.cursor.execute('''
            INSERT INTO positions (x, o, k_move)
            VALUES (?, ?, ?)
        ''', (x, o, k_move))
        self.connection.commit()

    def update_entry(self, x: int, o: int, k_move: int) -> None:
        """Updates an existing entry in the positions database."""
        self.cursor.execute('''
            UPDATE positions
            SET k_move = ?
            WHERE x = ? AND o = ?
        ''', (k_move, x, o))
        self.connection.commit()

    def add_board(self, board: Board, k_start: int, k_end: int, k_removal: int, outcome: int, depth: int) -> None:
        """Adds a board as a new entry to the positions database."""
        self.add_entry(board.x, board.o, self.intify(k_start, k_end, k_removal, outcome, depth) )

    def update_board(self, board: Board, k_start: int, k_end: int, k_removal: int, outcome: int, depth: int) -> None:
        """Updates a board entry in the positions database."""
        self.update_entry(board.x, board.o, self.intify(k_start, k_end, k_removal, outcome, depth) )

    def get_entry(self, x: int, o: int) -> tuple[int,int,int,int,int] | None:
        """Gets an entry in the positions database, or None if it doesn't exist."""
        self.cursor.execute('''
            SELECT k_move FROM positions
            WHERE x = ? AND o = ? 
        ''', (x, o,))
        result = self.cursor.fetchone()
        if result is None:
            return result
        else:
            return self.deintify(result[0])
        
    def get_entry_by_id(self, id: int) -> tuple[int,int,int]:
        """Gets an entry in the positions database by id."""
        self.cursor.execute('''
            SELECT x, o, k_move FROM positions
            WHERE id = ?
        ''', (id,))
        return self.cursor.fetchone()
        
    def get_board(self, board: Board) -> tuple[int,int,int,int,int] | None:
        """Gets a board in the positions database, or None if it doesn't exist."""
        return self.get_entry(board.x,board.o)
    
    def get_best_move(self, a_board: Board) -> tuple[int,int,int,int] | None:
        """Gets the equivalence board in the positions database, or None if it doesn't exist."""
        board = Board(a_board)
        xo_swapped = False
        if not board.xmove:
            board = self.rotator.swap_x_and_o(board)
            xo_swapped = True
        eq_board, r = self.rotator.get_equivalence_board(board)
        result = self.get_entry(eq_board.x,eq_board.o)
        if result is None:
            return None
        k_start_r, k_end_r, k_removal_r, outcome_r, depth = result
        k_start = self.rotator.inverse_index_rotation_list[r][k_start_r]
        k_end = self.rotator.inverse_index_rotation_list[r][k_end_r]
        k_removal = self.rotator.inverse_index_rotation_list[r][k_removal_r]
        outcome = -1*outcome_r if xo_swapped else outcome_r
        return (k_start,k_end,k_removal,outcome, depth)
    
    def add_best_move(self, a_board: Board, k_start: int, k_end: int, k_removal: int, outcome: int, depth: int) -> None:
        """Adds the equivalence board to the positions database, if it doesn't exist."""
        board = Board(a_board)
        xo_swapped = False
        if not board.xmove:
            board = self.rotator.swap_x_and_o(board)
            xo_swapped = True
        eq_board, r = self.rotator.get_equivalence_board(board)
        result = self.get_entry(eq_board.x,eq_board.o)
        if result is None:
            k_start_r = self.rotator.index_rotation_list[r][k_start]
            k_end_r = self.rotator.index_rotation_list[r][k_end]
            k_removal_r = self.rotator.index_rotation_list[r][k_removal] 
            outcome_r = -1*outcome if xo_swapped else outcome
            self.add_board(eq_board,k_start_r,k_end_r,k_removal_r,outcome_r,depth)

    def update_best_move(self, a_board: Board, k_start: int, k_end: int, k_removal: int, outcome: int, depth: int) -> None:
        """Updates the equivalence board in the positions database, or adds it if it doesn't exist."""
        board = Board(a_board)
        xo_swapped = False
        if not board.xmove:
            board = self.rotator.swap_x_and_o(board)
            xo_swapped = True
        eq_board, r = self.rotator.get_equivalence_board(board)
        k_start_r = self.rotator.index_rotation_list[r][k_start]
        k_end_r = self.rotator.index_rotation_list[r][k_end]
        k_removal_r = self.rotator.index_rotation_list[r][k_removal] 
        outcome_r = -1*outcome if xo_swapped else outcome
        self.update_board(eq_board,k_start_r,k_end_r,k_removal_r,outcome_r,depth)

    def display_entry(self, id: int, required_outcome = None) -> int:
        """Visually shows an entry from the database."""
        p1 = Player()
        p2 = Player()
        game = Game_Visual(p1,p2)
        result = self.get_entry_by_id(id)
        if result is None:
            print('Result is none!')
            return -1
        x, o, k_move = result
        k_start, k_end, k_removal, outcome, depth = self.deintify(k_move)
        if required_outcome is not None:
            if outcome != required_outcome:
                return 0
        game.board.x = x
        game.board.o = o
        game.board.xinhand = 0
        game.board.oinhand = 0
        game.board.save_state_to_history()
        game.board.move_x_by_k(k_start,k_end)
        game.board.save_state_to_history()
        print(f'Entry {id} - Projected outcome: {outcome}')
        game.replay_game()
        return 1

    
    def close(self):
        """Close the database."""
        self.connection.close()