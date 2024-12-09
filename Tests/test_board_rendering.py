import sys
import unittest
from io import StringIO

from src.simulation_from_chess import*
from src.simulation_from_chess.core import board, coordinates
from src.simulation_from_chess.entities import herbivore, grass, predator
from src.simulation_from_chess.renderers import board_console_renderer


class TestBoardRendering(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляры необходимых классов перед каждым тестом."""
        self.board = Board(3, 3)  # Доска размером 3x3
        self.renderer = BoardConsoleRenderer()

    def _capture_render_output(self, render_method, *args):
        """Вспомогательный метод для перехвата вывода рендерера."""
        original_stdout = sys.stdout
        output = StringIO()
        sys.stdout = output

        if args:
            render_method(*args)
        else:
            render_method()

        render_result = output.getvalue()
        sys.stdout = original_stdout
        return render_result

    def _get_cell(self, background_color, content):
        """Вспомогательный метод для создания клетки с заданным фоном и содержимым."""
        return f"{background_color}{content}{self.renderer.ANSI_RESET}"

    def _get_empty_cell(self, background_color):
        """Вспомогательный метод для создания пустой клетки."""
        return self._get_cell(background_color, self.renderer.EMPTY_CELL)

    def _get_entity_cell(self, background_color, entity_symbol):
        """Вспомогательный метод для создания клетки с существом."""
        return self._get_cell(background_color, f" {entity_symbol} ")

    def _get_board_row(self, rank, cells):
        """Вспомогательный метод для создания строки доски."""
        return f"{rank:2d} {''.join(cells)}\n"

    def _get_header_row(self):
        """Вспомогательный метод для создания строки с номерами столбцов."""
        col_numbers = "     " + f"  {self.renderer.WIDE_SPACE}{self.renderer.EN_SPACE}".join(
            f"{x}" for x in range(1, self.board.width + 1))
        return f"{col_numbers}\n"

    def test_empty_board_rendering(self):
        """Те��т на рендеринг пустой доски размером 3x3."""
        render_result = self._capture_render_output(
            self.renderer.render_without_entity,
            self.board
        )

        expected_output = []
        for rank in range(3, 0, -1):
            row_cells = []
            for file in range(1, 4):
                bg_color = (self.renderer.ANSI_BLACK_SQUARE_BACKGROUND 
                           if (rank + file) % 2 == 0 
                           else self.renderer.ANSI_WHITE_SQUARE_BACKGROUND)
                row_cells.append(self._get_empty_cell(bg_color))
            expected_output.append(self._get_board_row(rank, row_cells))
        expected_output.append(self._get_header_row())

        self.assertEqual(render_result, ''.join(expected_output))

    def test_board_with_herbivore(self):
        """Тест на рендеринг доски с травоядным."""
        herbivore = Herbivore(Coordinates(2, 2))
        self.board.set_piece(herbivore.coordinates, herbivore)

        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )

        expected_output = []
        for rank in range(3, 0, -1):
            row_cells = []
            for file in range(1, 4):
                bg_color = (self.renderer.ANSI_BLACK_SQUARE_BACKGROUND 
                           if (rank + file) % 2 == 0 
                           else self.renderer.ANSI_WHITE_SQUARE_BACKGROUND)
                if rank == 2 and file == 2:
                    row_cells.append(self._get_entity_cell(bg_color, "🐇"))
                else:
                    row_cells.append(self._get_empty_cell(bg_color))
            expected_output.append(self._get_board_row(rank, row_cells))
        expected_output.append(self._get_header_row())
        expected_output.append('\n')  # Добавляем пустую строку

        self.assertEqual(render_result, ''.join(expected_output))

    def test_render_after_movement(self):
        """Тест на корректный рендеринг доски после перемещения существа."""
        herbivore = Herbivore(Coordinates(1, 2))
        grass = Grass(Coordinates(2, 2))

        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)

        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )

        expected_output = []
        for rank in range(3, 0, -1):
            row_cells = []
            for file in range(1, 4):
                bg_color = (self.renderer.ANSI_BLACK_SQUARE_BACKGROUND 
                           if (rank + file) % 2 == 0 
                           else self.renderer.ANSI_WHITE_SQUARE_BACKGROUND)
                if rank == 2:
                    if file == 1:
                        row_cells.append(self._get_entity_cell(bg_color, "🐇"))
                    elif file == 2:
                        row_cells.append(self._get_entity_cell(bg_color, "🌾"))
                    else:
                        row_cells.append(self._get_empty_cell(bg_color))
                else:
                    row_cells.append(self._get_empty_cell(bg_color))
            expected_output.append(self._get_board_row(rank, row_cells))
        expected_output.append(self._get_header_row())
        expected_output.append('\n')  # Добавляем пустую строку

        self.assertEqual(render_result, ''.join(expected_output))




if __name__ == '__main__':
    unittest.main()
