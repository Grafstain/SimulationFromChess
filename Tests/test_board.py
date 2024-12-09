import unittest
import sys
import os

# Добавляем путь к корневой директории проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulation_from_chess.core.board import Board
from src.simulation_from_chess.core.coordinates import Coordinates
from src.simulation_from_chess.entities.grass import Grass
from src.simulation_from_chess.entities.herbivore import Herbivore
from src.simulation_from_chess.entities.stone import Stone

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения."""
        self.board_size = 5
        self.board = Board(self.board_size, self.board_size)

    def test_board_initialization(self):
        """Тест инициализации доски."""
        self.assertEqual(self.board.width, self.board_size)
        self.assertEqual(self.board.height, self.board_size)
        self.assertEqual(len(self.board.entities), 0)
        
        # Проверка невалидных размеров
        with self.assertRaises(ValueError):
            Board(0, 5)
        with self.assertRaises(ValueError):
            Board(5, 0)
        with self.assertRaises(ValueError):
            Board(-1, -1)

    def test_board_edge_cases(self):
        """Тест граничных случаев доски."""
        # Проверка координат за пределами доски
        invalid_coords = [
            Coordinates(0, 1),  # За левой границей
            Coordinates(self.board_size + 1, 1),  # За правой границей
            Coordinates(1, 0),  # За нижней границей
            Coordinates(1, self.board_size + 1),  # За верхней границей
        ]
        
        entity = Grass(Coordinates(1, 1))
        for coords in invalid_coords:
            with self.assertRaises(ValueError):
                self.board.place_entity(coords, entity)
        
        # Проверка переполнения доски
        valid_coords = Coordinates(1, 1)
        self.board.place_entity(valid_coords, entity)
        with self.assertRaises(ValueError):
            self.board.place_entity(valid_coords, Grass(valid_coords))
            
        # Проверка удаления несуществующих сущностей
        empty_coords = Coordinates(2, 2)
        self.assertFalse(self.board.remove_entity(empty_coords))

    def test_entity_placement_and_removal(self):
        """Тест размещения и удаления сущностей."""
        coords = Coordinates(1, 1)
        entity = Grass(coords)
        
        # Проверка размещения
        self.board.place_entity(coords, entity)
        self.assertEqual(self.board.get_entity(coords), entity)
        
        # Проверка удаления
        self.assertTrue(self.board.remove_entity(coords))
        self.assertIsNone(self.board.get_entity(coords))
        
        # Проверка размещения в ту же позицию после удаления
        new_entity = Stone(coords)
        self.board.place_entity(coords, new_entity)
        self.assertEqual(self.board.get_entity(coords), new_entity)

    def test_position_vacancy(self):
        """Тест проверки свободных позиций."""
        coords = Coordinates(1, 1)
        entity = Grass(coords)
        
        self.assertTrue(self.board.is_position_vacant(coords))
        
        self.board.place_entity(coords, entity)
        self.assertFalse(self.board.is_position_vacant(coords))
        
        self.board.remove_entity(coords)
        self.assertTrue(self.board.is_position_vacant(coords))

    def test_get_adjacent_positions(self):
        """Тест получения соседних позиций."""
        # Центральная позиция
        center = Coordinates(2, 2)
        adjacent = self.board.get_adjacent_positions(center)
        self.assertEqual(len(adjacent), 8)  # Все 8 соседних позиций
        
        # Угловая позиция
        corner = Coordinates(1, 1)
        corner_adjacent = self.board.get_adjacent_positions(corner)
        self.assertEqual(len(corner_adjacent), 3)  # Только 3 соседние позиции
        
        # Краевая позиция
        edge = Coordinates(1, 2)
        edge_adjacent = self.board.get_adjacent_positions(edge)
        self.assertEqual(len(edge_adjacent), 5)  # 5 соседних позиций

    def test_get_entities_by_type(self):
        """Тест получения сущностей по типу."""
        # Размещаем разные сущности
        self.board.place_entity(Coordinates(1, 1), Grass(Coordinates(1, 1)))
        self.board.place_entity(Coordinates(2, 2), Herbivore(Coordinates(2, 2)))
        self.board.place_entity(Coordinates(3, 3), Grass(Coordinates(3, 3)))
        
        # Проверяем фильтрацию по типу
        grass_entities = self.board.get_entities_by_type(Grass)
        self.assertEqual(len(grass_entities), 2)
        
        herbivore_entities = self.board.get_entities_by_type(Herbivore)
        self.assertEqual(len(herbivore_entities), 1)
        
        stone_entities = self.board.get_entities_by_type(Stone)
        self.assertEqual(len(stone_entities), 0)

    def test_board_clear(self):
        """Тест очистки доски."""
        # Размещаем сущности
        self.board.place_entity(Coordinates(1, 1), Grass(Coordinates(1, 1)))
        self.board.place_entity(Coordinates(2, 2), Stone(Coordinates(2, 2)))
        
        self.assertEqual(len(self.board.entities), 2)
        
        # Очищаем доску
        self.board.clear()
        self.assertEqual(len(self.board.entities), 0)