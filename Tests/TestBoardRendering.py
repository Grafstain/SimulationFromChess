import unittest
from io import StringIO
import sys

from Board import Board
from BoardConsoleRenderer import BoardConsoleRenderer
from Coordinates import Coordinates
from entities.Herbivore import Herbivore
from entities.Predator import Predator


class TestBoardRendering(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляры необходимых классов перед каждым тестом."""
        self.board = Board(3,3)  # Доска размером 3x3
        self.renderer = BoardConsoleRenderer()


    def test_empty_board_rendering(self):
        """Тест на рендеринг пустой доски размером 3x3."""
        expected_output = (
        f" 3  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f" 2  {self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f" 1  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f"      1   2   3\n"
        )
        original_stdout = sys.stdout
        output = StringIO()
        sys.stdout = output  # Перенаправляем stdout для проверки вывода

        self.renderer.render_without_entity(self.board)
        render_result = output.getvalue()
        sys.stdout = original_stdout  # Возвращаем stdout
        self.assertEqual(render_result, expected_output)


    def test_board_with_herbivore(self):
        """Тест на рендеринг доски с травоядным."""
        herbivore = Herbivore(Coordinates(2, 2))
        self.board.set_piece(herbivore.coordinates, herbivore)

        # Ожидаемый вывод с травоядным на позиции (2,2)
        expected_output = (
        f" 3  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f" 2  {self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND} 🐇 " + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f" 1  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" + f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
        f"      1   2   3\n"
        )

        original_stdout = sys.stdout
        output = StringIO()
        sys.stdout = output

        self.renderer.render_without_entity(self.board)
        render_result = output.getvalue()
        sys.stdout = original_stdout
        print()
        self.assertEqual(render_result, expected_output)
        print()


if __name__ == '__main__':
    unittest.main()