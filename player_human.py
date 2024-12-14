from player import Player
from board import Board

class Human(Player):
    def __init__(self, name: str, gui: bool = True) -> None:
        super().__init__()
        self.gui = gui
        self.name = name

    def get_input(self, prompt: str, expected_length: int, ranges: list[tuple[int, int]]) -> list[int]:
        """Helper function to validate player input."""
        while True:
            instring = input(f'{self.name}: {prompt}')
            if instring.lower() in {"quit", "q"}:
                confirm = input("Are you sure you want to quit? (y/n): ").lower()
                if confirm == 'y':
                    quit()
                else:
                    continue
            inputs = instring.split(",")
            if len(inputs) != expected_length:
                print(f"Invalid input format. Expected {expected_length} values separated by commas.")
                continue
            try:
                values = [int(inputs[i].strip()) for i in range(expected_length)]
            except ValueError:
                print("Invalid input: all values must be integers.")
                continue
            if all(r[0] <= values[i] <= r[1] for i, r in enumerate(ranges)):
                return values
            print("Invalid input: values out of range.")
    
    def get_placement(self, board: Board) -> list[int, int]:
        """Prompt the player to place a piece."""
        return self.get_input(
            "Type the placement of your rock (row, column): [row: 0-2, column: 0-7]",
            2,
            [(0, 2), (0, 7)]
        )
    
    def get_move(self, board: Board) -> list[int, int, int, int]:
        """Prompt the player to move a piece."""
        return self.get_input(
            "Type the rock to move and the direction (row, column, direction): [row: 0-2, column: 0-7, new row: 0-2, new column: 0-7]",
            4,
            [(0, 2), (0, 7), (0, 2), (0, 7)]
        )
    
    def get_removal(self, board: Board) -> list[int, int]:
        """Prompt the player to remove an opponent's piece."""
        return self.get_input(
            "Type the location of the opponent's rock to remove (row, column): [row: 0-2, column: 0-7]",
            2,
            [(0, 2), (0, 7)]
        )
