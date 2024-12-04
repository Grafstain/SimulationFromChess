from Board import Board
from Coordinates import Coordinates
from Herbivore import Herbivore
from Predator import Predator


class BoardConsoleRenderer:
    ANSI_RESET = "\u001B[0m"
    ANSI_WHITE_SQUARE_BACKGROUND = "\u001B[47m"
    ANSI_BLACK_SQUARE_BACKGROUND = "\u001B[0;100m"
    ANSI_YELLOW_ENTITY_COLOR = "\u001B[33m"
    ANSI_RED_ENTITY_COLOR = "\u001B[31m"
    ANSI_WHITE_ENTITY_COLOR = "\u001B[97m"
    ANSI_BLACK_ENTITY_COLOR = "\u001B[30m"
    TAB = '\t'

    def render(self, board):
        # print("Rendering board...")
        for rank in range(8, 0, -1):
            line = ""
            for file in range(1, 9):  # Предположим, что файлы от 1 до 8
                coordinates = Coordinates(file, rank)
                if board.is_square_empty(coordinates):
                    line += self.get_sprite_for_empty_square(coordinates)
                else:
                    entity = board.get_piece(coordinates)
                    line += self.get_entity_sprite(entity)

            line += self.ANSI_RESET
            print(line)

    def render_without_entity(self, board):
        self.render(board)

    def get_sprite_for_empty_square(self, coordinates: Coordinates) -> str:
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if Board.is_square_dark(
            coordinates) else self.ANSI_WHITE_SQUARE_BACKGROUND
        return f"{background_color}  {self.TAB}{self.ANSI_RESET}"

    def select_ascii_sprite_for_entity(self, entity) -> str:
        if isinstance(entity, Herbivore):
            return f"{self.ANSI_WHITE_ENTITY_COLOR}🐑"
        if isinstance(entity, Predator):
            return f"{self.ANSI_RED_ENTITY_COLOR}🐺"

    def get_entity_sprite(self, entity) -> str:
        sprite = f" {self.select_ascii_sprite_for_entity(entity)} "
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if Board.is_square_dark(
            entity.coordinates) else self.ANSI_WHITE_SQUARE_BACKGROUND
        return f"{background_color}{sprite}{self.ANSI_RESET}"
