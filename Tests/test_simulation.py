from Tests import *


class TestSimulation(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляры необходимых классов перед каждым тестом."""
        self.board = Board(3,3)
        self.renderer = BoardConsoleRenderer()
        # self.herbivore = Herbivore(Coordinates(1, 1))
        # self.predator = Predator(Coordinates(2, 2))

    def test_empty_board_rendering(self):
        """Тест на рендеринг пустой доски."""
        output = StringIO()
        sys.stdout = output  # Перенаправляем stdout для проверки вывода
        self.renderer.render_without_entity(self.board)
        sys.stdout = sys.__stdout__  # Возвращаем stdout

        expected_output = (f""" 3    	  	  	
 2    	  	  	
 1    	  	  	
      1   2   3"""
                           )
  # Ожидаемый вывод для пустой доски
        print()
        self.assertIn(expected_output, output.getvalue())

    # def test_add_entity_to_board(self):
    #     """Тест на установку существа на доску."""
    #     self.board.set_piece(self.herbivore.coordinates, self.herbivore)
    #
    #     # Проверяем, что существо установлено на доске
    #     self.assertEqual(self.board.get_piece(self.herbivore.coordinates), self.herbivore)

    # def test_herbivore_movement(self):
    #     """Тест на движение травоядного и проверка состояния доски после движения."""
    #     self.board.set_piece(self.herbivore.coordinates, self.herbivore)
    #     grass = Grass(Coordinates(2, 1))  # Добавляем траву рядом
    #     self.board.set_piece(grass.coordinates, grass)
    #
    #     # Перемещение травоядного
    #     self.herbivore.make_move(self.board)
    #
    #     # Проверяем новое положение травоядного
    #     new_coordinates = Coordinates(2, 1)  # Ожидаемое новое положение
    #     self.assertEqual(self.herbivore.coordinates, new_coordinates)
    #
    #     # Проверяем состояние доски после движения
    #     output = StringIO()
    #     sys.stdout = output  # Перенаправляем stdout для проверки вывода
    #     self.renderer.render(self.board)
    #     sys.stdout = sys.__stdout__  # Возвращаем stdout
    #
    #     expected_output_after_move = "..."  # Ожидаемый вывод после движения
    #     self.assertIn(expected_output_after_move, output.getvalue())


if __name__ == '__main__':
    unittest.main()