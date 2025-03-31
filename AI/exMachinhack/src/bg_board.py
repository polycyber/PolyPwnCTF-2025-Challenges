import json

from seahorse.game.game_layout.board import Board, Piece
from seahorse.utils.serializer import Serializable


class BGBoard(Board):
    """
    A class representing a game board.

    Attributes:
        env (dict[Tuple[int], Piece]): The environment dictionary composed of pieces.
        dimensions (list[int]): The dimensions of the board.
    """

    def __init__(self, env: dict[tuple[int], Piece], dim: list[int]) -> None:
        """
        Initializes a new instance of the BoardTictac class.

        Args:
            env (dict[Tuple[int], Piece]): The environment dictionary composed of pieces.
            dim (list[int]): The dimensions of the board.
        """
        super().__init__(env, dim)

    def __str__(self) -> str:
         # ANSI escape codes for colors
        RED = '\033[91m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        EMPTY = '·'  # Symbol for empty cell

        board_representation = "\n"
        env = self.get_env()
        dimensions = self.get_dimensions()

        for row in range(dimensions[0]):
            for col in range(dimensions[1]):
                piece = env.get((row, col))
                if piece is None:
                    board_representation += f"{EMPTY} "
                elif piece.piece_type == "W":
                    board_representation += f"{RED}●{RESET} "
                elif piece.piece_type == "B":
                    board_representation += f"{YELLOW}●{RESET} "
            board_representation += "\n"
        board_representation += "1 2 3 4 5 6 7\n"
        return board_representation

    def to_json(self) -> dict:
        """
        Converts the board to a JSON object.

        Returns:
            dict: The JSON representation of the board.
        """
        return {"env":{str(x):y for x,y in self.env.items()},"dim":self.dimensions}

    @classmethod
    def from_json(cls, data) -> Serializable:
        d = json.loads(data)
        dd = json.loads(data)
        for x,y in d["env"].items():
            # TODO eval is unsafe
            del dd["env"][x]
            dd["env"][eval(x)] = Piece.from_json(json.dumps(y))
        return cls(**dd)
