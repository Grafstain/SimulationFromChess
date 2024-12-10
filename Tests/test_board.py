import unittest
from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.predator import Predator
from src.simulation_from_chess.entities.grass import Grass

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения."""
        self.board = Board(5, 5)  # Уменьшенное поле для тестов
        
    def test_board_initialization(self):
        """Тест инициализации доски."""
        self.assertEqual(self.board.width, 5)
        self.assertEqual(self.board.height, 5)
        self.assertEqual(len(self.board.entities), 0)
        
    def test_invalid_board_size(self):
        """Тест создания доски с невалидными размерами."""
        with self.assertRaises(ValueError):
            Board(0, 5)
        with self.assertRaises(ValueError):
            Board(5, 0)
            
    def test_place_entity(self):
        """Тест размещения сущности на доске."""
        entity = Herbivore(Coordinates(1, 1))
        self.board.place_entity(entity.coordinates, entity)
        self.assertIn(entity.coordinates, self.board.entities)
        self.assertEqual(self.board.entities[entity.coordinates], entity)
        
    def test_place_entity_occupied_cell(self):
        """Тест размещения сущности на занятую клетку."""
        coords = Coordinates(1, 1)
        entity1 = Herbivore(coords)
        entity2 = Predator(coords)
        
        self.board.place_entity(coords, entity1)
        with self.assertRaises(ValueError) as context:
            self.board.place_entity(coords, entity2)
        
        # Проверяем сообщение об ошибке
        self.assertIn("уже занята", str(context.exception))
        
        # Проверяем, что первая сущность осталась на месте
        self.assertEqual(self.board.get_entity(coords), entity1)
            
    def test_remove_entity(self):
        """Тест удаления сущности с доски."""
        entity = Herbivore(Coordinates(1, 1))
        self.board.place_entity(entity.coordinates, entity)
        self.board.remove_entity(entity.coordinates)
        self.assertNotIn(entity.coordinates, self.board.entities)
        
    def test_get_entity(self):
        """Тест получения сущности по координатам."""
        entity = Herbivore(Coordinates(1, 1))
        self.board.place_entity(entity.coordinates, entity)
        retrieved_entity = self.board.get_entity(entity.coordinates)
        self.assertEqual(entity, retrieved_entity)
        
    def test_get_nonexistent_entity(self):
        """Тест получения несуществующей сущности."""
        entity = self.board.get_entity(Coordinates(1, 1))
        self.assertIsNone(entity)
        
    def test_get_entities_by_type(self):
        """Тест получения сущностей определенного типа."""
        herb = Herbivore(Coordinates(1, 1))
        pred = Predator(Coordinates(2, 2))
        grass = Grass(Coordinates(3, 3))
        
        self.board.place_entity(herb.coordinates, herb)
        self.board.place_entity(pred.coordinates, pred)
        self.board.place_entity(grass.coordinates, grass)
        
        herbivores = self.board.get_entities_by_type(Herbivore)
        predators = self.board.get_entities_by_type(Predator)
        grasses = self.board.get_entities_by_type(Grass)
        
        self.assertEqual(len(herbivores), 1)
        self.assertEqual(len(predators), 1)
        self.assertEqual(len(grasses), 1)
        
    def test_get_empty_cells(self):
        """Тест получения пустых клеток."""
        # Проверяем начальное количество пустых клеток
        initial_empty = len(self.board.get_empty_cells())
        self.assertEqual(initial_empty, self.board.width * self.board.height)
        
        # Размещаем сущность
        entity = Herbivore(Coordinates(1, 1))
        self.board.place_entity(entity.coordinates, entity)
        
        # Проверяем, что количество пустых клеток уменьшилось
        new_empty = len(self.board.get_empty_cells())
        self.assertEqual(new_empty, initial_empty - 1)
        
        # Проверяем, что занятая клетка не входит в список пустых
        empty_cells = self.board.get_empty_cells()
        self.assertNotIn(entity.coordinates, empty_cells)
        
    def test_manhattan_distance(self):
        """Тест расчета манхэттенского расстояния."""
        test_cases = [
            (Coordinates(1, 1), Coordinates(4, 5), 7),  # |4-1| + |5-1| = 3 + 4 = 7
            (Coordinates(2, 2), Coordinates(2, 5), 3),  # |2-2| + |5-2| = 0 + 3 = 3
            (Coordinates(1, 1), Coordinates(1, 1), 0),  # |1-1| + |1-1| = 0 + 0 = 0
            (Coordinates(5, 5), Coordinates(1, 1), 8)   # |1-5| + |1-5| = 4 + 4 = 8
        ]
        
        for coords1, coords2, expected in test_cases:
            distance = self.board.manhattan_distance(coords1, coords2)
            self.assertEqual(
                distance, 
                expected,
                f"Неверное расстояние между {coords1} и {coords2}"
            )
        
    def test_next_turn(self):
        """Тест перехода к следующему ходу."""
        initial_turn = self.board.game_state.current_turn
        self.board.next_turn()
        self.assertEqual(self.board.game_state.current_turn, initial_turn + 1)

if __name__ == '__main__':
    unittest.main()