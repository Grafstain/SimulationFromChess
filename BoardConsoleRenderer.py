from entities.Grass import Grass
from entities.Stone import Stone
from Board import Board
from Coordinates import Coordinates
from entities.Herbivore import Herbivore
from entities.Predator import Predator


class BoardConsoleRenderer:
    ANSI_RESET = "\u001B[0m"
    ANSI_WHITE_SQUARE_BACKGROUND = "\u001B[47m"
    ANSI_BLACK_SQUARE_BACKGROUND = "\u001B[0;100m"
    ANSI_WHITE_ENTITY_COLOR = "\u001B[97m"
    ANSI_BLACK_ENTITY_COLOR = "\u001B[30m"
    TAB = '\t'

    def render(self, board):
        # print("Rendering board...")
        for rank in range(8, 0, -1):
            line = f"{rank:2}  "
            for file in range(1, 9):  # Предположим, что файлы от 1 до 8
                coordinates = Coordinates(file, rank)
                if board.is_square_empty(coordinates):
                    line += self.get_sprite_for_empty_square(coordinates)
                else:
                    entity = board.get_piece(coordinates)
                    line += self.get_entity_sprite(entity)
            line += self.ANSI_RESET
            print(line)
        # Выводим заголовок для столбцов
        header = "    " + " ".join(f"{i + 1:3}" for i in range(board.width))  # Заголовок столбцов с выравниванием
        print(header)
        # self.display_log(board)
        self.display_common_creature_info(board)
        print()

    def render_without_entity(self, board):
        self.render(board)

    def get_sprite_for_empty_square(self, coordinates: Coordinates) -> str:
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if Board.is_square_dark(
            coordinates) else self.ANSI_WHITE_SQUARE_BACKGROUND
        return f"{background_color}  {self.TAB}{self.ANSI_RESET}"

    def select_ascii_sprite_for_entity(self, entity) -> str:
        if isinstance(entity, Herbivore):
            return "🐇"
        if isinstance(entity, Predator):
            return "🐅"
        if isinstance(entity, Grass):
            return "🌾"
        if isinstance(entity, Stone):
            return "🌑"


    def get_entity_sprite(self, entity) -> str:
        sprite = f" {self.select_ascii_sprite_for_entity(entity)} "
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if Board.is_square_dark(
            entity.coordinates) else self.ANSI_WHITE_SQUARE_BACKGROUND
        return f"{background_color}{sprite}{self.ANSI_RESET}"

    @staticmethod
    def display_log(board):
        print("Объекты на поле:")
        for rank in range(8, 0, -1):
            for file in range(1, 9):
                coordinates = Coordinates(file, rank)
                if not board.is_square_empty(coordinates):
                    entity = board.get_piece(coordinates)
                    if isinstance(entity, (Herbivore, Predator)):
                        print(f"{entity}\t{entity.coordinates}\t{entity.hp} energy")

    @staticmethod
    def display_common_creature_info(board):
        print("Объекты на поле:")
        herbivore_count = sum(1 for entity in board.entities.values() if isinstance(entity, Herbivore))
        predator_count = sum(1 for entity in board.entities.values() if isinstance(entity, Predator))
        grass_count = sum(1 for entity in board.entities.values() if isinstance(entity, Grass))
        print(f"Herbivore:\t{herbivore_count}\n"
              f"Predator:\t{predator_count}\n"
              f"Grass:\t\t{grass_count}")
