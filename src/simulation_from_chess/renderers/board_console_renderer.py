from ..entities import *
from ..core import *


class BoardConsoleRenderer:
    ANSI_RESET = "\u001B[0m"
    ANSI_WHITE_SQUARE_BACKGROUND = "\u001B[47m"
    ANSI_BLACK_SQUARE_BACKGROUND = "\u001B[0;100m"
    WIDE_SPACE = '\u2005'
    EN_SPACE = "\u2002"
    EMPTY_CELL = f"  {WIDE_SPACE}{EN_SPACE} "

    def get_background_color(self, coordinates: Coordinates) -> str:
        """Возвращает цвет фона для клетки."""
        return (self.ANSI_BLACK_SQUARE_BACKGROUND 
                if self.is_square_dark(coordinates)
                else self.ANSI_WHITE_SQUARE_BACKGROUND)

    def get_entity_symbol(self, entity) -> str:
        """Возвращает символ для сущности."""
        if entity is None:
            return self.EMPTY_CELL
        return f" {self.select_ascii_sprite_for_entity(entity)} "

    def render(self, board):
        """Отрисовка игрового поля."""
        output = []
        # Отрисовка поля сверху вниз
        for y in range(board.height, 0, -1):
            row = f"{y:2d} "
            for x in range(1, board.width + 1):
                coord = Coordinates(x, y)
                entity = board.get_entity(coord)
                bg_color = self.get_background_color(coord)
                cell = f"{bg_color}{self.get_entity_symbol(entity)}{self.ANSI_RESET}"
                row += cell
            output.append(row)
        
        # Добавление нумерации столбцов
        col_numbers = "     " + f"  {self.WIDE_SPACE}{self.EN_SPACE}".join(f"{x}" for x in range(1, board.width + 1))
        output.append(col_numbers)
        
        # Выводим поле
        rendered_board = "\n".join(output)
        print(rendered_board)
        print()
        
        return rendered_board

    def render_without_entity(self, board):
        """Рендерит только пустую доску без существ"""
        output = []
        for rank in range(board.height, 0, -1):
            row = f"{rank:2d} "
            for file in range(1, board.width + 1):
                coordinates = Coordinates(file, rank)
                bg_color = self.get_background_color(coordinates)
                cell = f"{bg_color}{self.EMPTY_CELL}{self.ANSI_RESET}"
                row += cell
            output.append(row)
        
        # Добавление нумерации столбцов
        col_numbers = "     " + f"  {self.WIDE_SPACE}{self.EN_SPACE}".join(f"{x}" for x in range(1, board.width + 1))
        output.append(col_numbers)
        
        # Выводим поле
        rendered_board = "\n".join(output)
        print(rendered_board)
        
        return rendered_board

    def select_ascii_sprite_for_entity(self, entity) -> str:
        """Возвращает символ для сущности."""
        if isinstance(entity, Herbivore):
            return "🐇"
        if isinstance(entity, Predator):
            return "🐅"
        if isinstance(entity, Grass):
            return "🌾"
        if isinstance(entity, Stone):
            return "🌑"

    @staticmethod
    def is_square_dark(coordinates: Coordinates) -> bool:
        """Определяет, является ли клетка темной."""
        return (coordinates.x + coordinates.y) % 2 == 0

    def get_entity_sprite(self, entity) -> str:
        sprite = f" {self.select_ascii_sprite_for_entity(entity)} "
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if self.is_square_dark(
            entity.coordinates) else self.ANSI_WHITE_SQUARE_BACKGROUND
        return f"{background_color}{sprite}"

    @staticmethod
    def display_log(board):
        """Отображение информации о существах."""
        print("\nОбъекты на поле:")
        for coordinates, entity in board.entities.items():
            if isinstance(entity, (Herbivore, Predator)):
                print(f"{entity}\t({coordinates.x}, {coordinates.y})\t{entity.hp} energy")
        print()  # Пустая строка после лога

    @staticmethod
    def display_common_creature_info(board):
        print("Объекты на поле:")
        herbivore_count = sum(1 for entity in board.entities.values() if isinstance(entity, Herbivore))
        predator_count = sum(1 for entity in board.entities.values() if isinstance(entity, Predator))
        grass_count = sum(1 for entity in board.entities.values() if isinstance(entity, Grass))
        print(f"Herbivore:\t{herbivore_count}\n"
              f"Predator:\t{predator_count}\n"
              f"Grass:\t\t{grass_count}")
