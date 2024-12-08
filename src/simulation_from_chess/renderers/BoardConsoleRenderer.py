from ..entities import *
from ..core import *


class BoardConsoleRenderer:
    ANSI_RESET = "\u001B[0m"
    ANSI_WHITE_SQUARE_BACKGROUND = "\u001B[47m"
    ANSI_BLACK_SQUARE_BACKGROUND = "\u001B[0;100m"
    WIDE_SPACE = '\u2005'
    EN_SPACE = "\u2002"

    def get_background_color(self, coordinates: Coordinates) -> str:
        """Возвращает цвет фона для клетки."""
        return (self.ANSI_BLACK_SQUARE_BACKGROUND 
                if Board.is_square_dark(coordinates) 
                else self.ANSI_WHITE_SQUARE_BACKGROUND)

    def get_entity_symbol(self, entity) -> str:
        """Возвращает символ для сущности."""
        if entity is None:
            return f"   {self.WIDE_SPACE}{self.EN_SPACE}"  # Три специальных пробела
        return f" {self.select_ascii_sprite_for_entity(entity)} "  # Существо между пробелами

    def render(self, board):
        """Отрисовка игрового поля."""
        output = []
        # Отрисовка поля сверху вниз
        for y in range(board.height, 0, -1):
            row = f"{y:2d} "
            for x in range(1, board.width + 1):
                coord = Coordinates(x, y)
                entity = board.get_piece(coord)
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
        print()  # Пустая строка для разделения с логом
        
        return rendered_board

    def render_without_entity(self, board):
        """Рендерит только пустую доску без существ"""
        for rank in range(board.height, 0, -1):
            line = f"{rank:2}"
            for file in range(1, board.width+1):
                coordinates = Coordinates(file, rank)
                line += self.get_sprite_for_empty_square(coordinates)
            line += self.ANSI_RESET
            print(line)
        header = "    " + " ".join(f"{i + 1:3}" for i in range(board.width))
        print(header)

    def get_sprite_for_empty_square(self, coordinates: Coordinates) -> str:
        """Возвращает спрайт для пустой клетки."""
        background_color = self.get_background_color(coordinates)
        return f"{background_color}{self.EM_SPACE}{self.EM_SPACE}{self.EM_SPACE}{self.ANSI_RESET}"

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

    def get_entity_sprite(self, entity) -> str:
        sprite = f" {self.select_ascii_sprite_for_entity(entity)} "
        background_color = self.ANSI_BLACK_SQUARE_BACKGROUND if Board.is_square_dark(
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
        print("Объек��ы на поле:")
        herbivore_count = sum(1 for entity in board.entities.values() if isinstance(entity, Herbivore))
        predator_count = sum(1 for entity in board.entities.values() if isinstance(entity, Predator))
        grass_count = sum(1 for entity in board.entities.values() if isinstance(entity, Grass))
        print(f"Herbivore:\t{herbivore_count}\n"
              f"Predator:\t{predator_count}\n"
              f"Grass:\t\t{grass_count}")
