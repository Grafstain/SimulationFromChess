import unittest
from io import StringIO
import sys

from Board import Board
from BoardConsoleRenderer import BoardConsoleRenderer
from Coordinates import Coordinates
from entities.Herbivore import Herbivore
from entities.Predator import Predator
from entities.Grass import Grass


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

    def _get_empty_board_output(self):
        """Возвращает ожидаемый вывод для пустой доски."""
        return (
                f" 3  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f" 2  {self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f" 1  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f"      1   2   3\n"
        )

    def test_empty_board_rendering(self):
        """Тест на рендеринг пустой доски размером 3x3."""
        render_result = self._capture_render_output(
            self.renderer.render_without_entity,
            self.board
        )
        self.assertEqual(render_result, self._get_empty_board_output())

    def test_board_with_herbivore(self):
        """Тест на рендеринг доски с травоядным."""
        herbivore = Herbivore(Coordinates(2, 2))
        self.board.set_piece(herbivore.coordinates, herbivore)

        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )

        expected_output = (
                f" 3  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f" 2  {self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND} 🐇 " +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f" 1  {self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_WHITE_SQUARE_BACKGROUND}  {self.renderer.TAB}" +
                f"{self.renderer.ANSI_BLACK_SQUARE_BACKGROUND}  {self.renderer.TAB}{self.renderer.ANSI_RESET}\n" +
                f"      1   2   3\n"
        )
        self.assertEqual(render_result, expected_output)

    def test_render_after_movement(self):
        """Тест на корректный рендеринг доски после перемещения существа."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(2, 2))

        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        herbivore.make_move(self.board)
        expected_output = (
                f" 3  \x1b[0;100m  	\x1b[47m  	\x1b[0;100m  	\x1b[0m\n" +
                f" 2  \x1b[47m 🐇 \x1b[0;100m 🌾 \x1b[47m  	\x1b[0m\n"
                f" 1  \x1b[0;100m  	\x1b[47m  	\x1b[0;100m  	\x1b[0m\n" +
                f"      1   2   3\n"
        )
        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )

        self.assertEqual(render_result, expected_output)


    def test_render_predator_movement(self):
        """Тест на корректный рендеринг доски после перемещения хищника."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(3, 3))

        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        predator.make_move(self.board)

        expected_output = (
                f" 3  \x1b[0;100m 🐅 \x1b[47m  \t\x1b[0;100m 🐇 \x1b[0m\n" +
                f" 2  \x1b[47m  \t\x1b[0;100m  \t\x1b[47m  	\x1b[0m\n"
                f" 1  \x1b[0;100m  	\x1b[47m  	\x1b[0;100m  	\x1b[0m\n" +
                f"      1   2   3\n"
        )
        render_result = self._capture_render_output(
            self.renderer.render,
            self.board
        )
        self.assertEqual(render_result, expected_output)




if __name__ == '__main__':
    unittest.main()
