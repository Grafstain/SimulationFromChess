import sys
import unittest
from io import StringIO
from unittest.mock import patch

from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.entities.stone import Stone
from src.simulation_from_chess.renderers.board_console_renderer import BoardConsoleRenderer


class TestBoardRendering(unittest.TestCase):
    def setUp(self) -> None:
        """Подготовка тестового окружения."""
        self.board = Board(3, 3)  # Уменьшенный размер для тестов
        self.renderer = BoardConsoleRenderer()

    def _capture_render_output(self, render_func, *args) -> str:
        """Захват вывода рендеринга."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            render_func(*args)
            return fake_output.getvalue()

    def _get_empty_cell(self, bg_color: str) -> str:
        """Получение пустой клетки с заданным цветом фона."""
        return f"{bg_color}{self.renderer.EMPTY_CELL}{self.renderer.ANSI_RESET}"

    def _get_entity_cell(self, bg_color: str, symbol: str) -> str:
        """Получение клетки с сущностью."""
        return f"{bg_color} {symbol} {self.renderer.ANSI_RESET}"

    def _get_board_row(self, rank: int, cells: list) -> str:
        """Получение строки доски."""
        return f"{rank:2d} {''.join(cells)}\n"

    def _get_header_row(self) -> str:
        """Получение строки с заголовками столбцов."""
        return "     " + f"  {self.renderer.WIDE_SPACE}{self.renderer.EN_SPACE}".join(str(i) for i in range(1, 4)) + "\n"

    def test_empty_board_rendering(self):
        """Тест рендеринга пустой доски."""
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
                row_cells.append(self._get_empty_cell(bg_color))
            expected_output.append(self._get_board_row(rank, row_cells))
        expected_output.append(self._get_header_row())
        expected_output.append('\n')

        self.assertEqual(render_result, ''.join(expected_output))

    def test_board_with_herbivore(self):
        """Тест на рендеринг доски с травоядным."""
        herbivore = Herbivore(Coordinates(2, 2))
        self.board.place_entity(herbivore.coordinates, herbivore)

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
        expected_output.append('\n')

        self.assertEqual(render_result, ''.join(expected_output))

    def test_render_after_movement(self):
        """Тест на корректный рендеринг доски после перемещения существа."""
        herbivore = Herbivore(Coordinates(1, 2))
        grass = Grass(Coordinates(2, 2))

        self.board.place_entity(herbivore.coordinates, herbivore)
        self.board.place_entity(grass.coordinates, grass)

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
        expected_output.append('\n')

        self.assertEqual(render_result, ''.join(expected_output))

    def test_render_statistics(self):
        """Тест отображения статистики."""
        # Проверка вывода количества существ
        # Проверка форматирования

    def test_render_different_entities(self):
        """Тест отображения разных типов сущностей."""
        # Размещаем разные типы сущностей с правильными символами
        entities = [
            (Herbivore(Coordinates(1, 1)), "🐇"),
            (Predator(Coordinates(1, 2)), "🐅"),
            (Grass(Coordinates(2, 1)), "🌾"),
            (Stone(Coordinates(2, 2)), "🌑")
        ]
        
        # Очищаем доску перед каждым тестом
        self.board.clear()
        
        for entity, symbol in entities:
            self.board.place_entity(entity.coordinates, entity)
            
            render_result = self._capture_render_output(
                self.renderer.render,
                self.board
            )
            
            # Проверяем, что символ сущности присутствует в выводе
            self.assertIn(
                symbol, 
                render_result,
                f"Символ {symbol} для {entity.__class__.__name__} не найден в выводе"
            )
            
            # Проверяем корректность цветового оформления
            bg_color = (self.renderer.ANSI_BLACK_SQUARE_BACKGROUND 
                       if (entity.coordinates.x + entity.coordinates.y) % 2 == 0 
                       else self.renderer.ANSI_WHITE_SQUARE_BACKGROUND)
            cell = self._get_entity_cell(bg_color, symbol)
            self.assertIn(cell, render_result)
            
            # Проверяем корректность нумерации столбцов
            expected_header = "     " + f"  {self.renderer.WIDE_SPACE}{self.renderer.EN_SPACE}".join(
                str(i) for i in range(1, self.board.width + 1)
            ) + "\n"
            self.assertIn(expected_header, render_result)
            
            # Проверяем корректность нумерации строк
            for rank in range(1, self.board.height + 1):
                self.assertIn(f"{rank:2d}", render_result)

    def test_render_board_borders(self):
        """Тест отображения границ доски."""
        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )
        
        # Проверка нумерации строк
        for rank in range(1, self.board.height + 1):
            self.assertIn(
                str(rank), 
                render_result,
                f"Номер строки {rank} не найден в выводе"
            )
        
        # Проверка нумерации столбцов
        for column in range(1, self.board.width + 1):
            self.assertIn(
                str(column),
                render_result, 
                f"Номер столбца {column} не найден в выводе"
            )
        
        # Проверка разделителей
        self.assertIn(
            self.renderer.ANSI_RESET, 
            render_result,
            "Отсут��твует сброс цветового оформления"
        )
        
        # Проверка переносов строк
        expected_lines = self.board.height + 2  # строки + заголовок + пустая строка
        actual_lines = render_result.count('\n')
        self.assertEqual(
            actual_lines, 
            expected_lines,
            f"Неверное количество строк: ожидалось {expected_lines}, получено {actual_lines}"
        )

    def test_empty_board(self):
        """Тест отображения пустой доски."""
        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )
        
        # Проверяем, что все клетки пустые
        for rank in range(1, self.board.height + 1):
            for file in range(1, self.board.width + 1):
                bg_color = (self.renderer.ANSI_BLACK_SQUARE_BACKGROUND 
                           if (rank + file) % 2 == 0 
                           else self.renderer.ANSI_WHITE_SQUARE_BACKGROUND)
                empty_cell = self._get_empty_cell(bg_color)
                self.assertIn(
                    empty_cell,
                    render_result,
                    f"Пустая клетка с цветом {bg_color} не найдена на позиции {file},{rank}"
                )

    def test_invalid_board_size(self):
        """Тест обработки некорректного размера доски."""
        with self.assertRaises(ValueError):
            Board(0, 3)
        with self.assertRaises(ValueError):
            Board(3, 0)
        with self.assertRaises(ValueError):
            Board(-1, -1)




if __name__ == '__main__':
    unittest.main()
