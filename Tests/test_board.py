from unittest import TestCase
from src.simulation_from_chess import Board, Coordinates, Herbivore, Predator, Grass, Stone
from src.simulation_from_chess.entities.entity import Entity

class TestBoard(TestCase):
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
        with self.assertRaises(ValueError):
            Board(-1, 5)
        with self.assertRaises(ValueError):
            Board(5, -1)
            
    def test_place_entity(self):
        """Тест размещения сущности на доске."""
        entity = Herbivore(Coordinates(1, 1))
        self.board.place_entity(entity.coordinates, entity)
        self.assertIn(entity.coordinates, self.board.entities)
        self.assertEqual(self.board.entities[entity.coordinates], entity)
        
    def test_place_entity_invalid_coordinates(self):
        """Тест размещения сущности с невалидными координатами."""
        invalid_coords = [
            Coordinates(0, 1),    # x < 1
            Coordinates(6, 1),    # x > width
            Coordinates(1, 0),    # y < 1
            Coordinates(1, 6),    # y > height
            Coordinates(0, 0),    # обе координаты < 1
            Coordinates(6, 6),    # обе координаты > размера
            Coordinates(-1, 1),   # отрицательные координаты
            Coordinates(1, -1)
        ]
        
        for coords in invalid_coords:
            entity = Herbivore(coords)
            with self.assertRaises(ValueError) as context:
                self.board.place_entity(coords, entity)
            self.assertIn(
                "невалидные координаты",
                str(context.exception).lower(),
                f"Неверное сообщение об ошибке для координат {coords}"
            )
        
    def test_place_entity_occupied_cell(self):
        """Тест размещения сущности на занятую клетку."""
        coords = Coordinates(1, 1)
        entity1 = Herbivore(coords)
        entity2 = Predator(coords)
        
        self.board.place_entity(coords, entity1)
        with self.assertRaises(ValueError) as context:
            self.board.place_entity(coords, entity2)
        
        error_message = str(context.exception)
        self.assertTrue(
            any(phrase in error_message.lower() for phrase in ["занята", "occupied"]),
            f"Сообщение об ошибке '{error_message}' не содержит информацию о занятой позиции"
        )
        self.assertEqual(self.board.get_entity(coords), entity1)
        
    def test_is_position_vacant(self):
        """Тест проверки свободной позиции."""
        coords = Coordinates(1, 1)
        entity = Herbivore(coords)
        
        self.assertTrue(self.board.is_position_vacant(coords))
        self.board.place_entity(coords, entity)
        self.assertFalse(self.board.is_position_vacant(coords))
        
    def test_is_valid_coordinates(self):
        """Тест проверки валидности координат."""
        # Проверяем валидные координаты
        valid_coords = [
            Coordinates(1, 1),  # Минимальные координаты
            Coordinates(5, 5),  # Максимальные координаты
            Coordinates(3, 3),  # Середина доски
            Coordinates(1, 5),  # Граничные случаи
            Coordinates(5, 1)
        ]
        
        # Проверяем невалидные координаты
        invalid_coords = [
            Coordinates(0, 1),    # x < 1
            Coordinates(6, 1),    # x > width
            Coordinates(1, 0),    # y < 1
            Coordinates(1, 6),    # y > height
            Coordinates(0, 0),    # обе координаты < 1
            Coordinates(6, 6),    # обе координаты > размера
            Coordinates(-1, 1),   # отрицательные координаты
            Coordinates(1, -1)
        ]
        
        # Проверяем валидные координаты
        for coords in valid_coords:
            self.assertTrue(
                self.board.is_valid_coordinates(coords),
                f"Координаты {coords} должны быть валидными"
            )
        
        # Проверяем невалидные координаты
        for coords in invalid_coords:
            self.assertFalse(
                self.board.is_valid_coordinates(coords),
                f"Координаты {coords} должны быть невалидными"
            )
        
    def test_get_entities_by_type(self):
        """Тест получения сущностей определенного типа."""
        entities = {
            Herbivore: [Coordinates(1, 1), Coordinates(2, 2)],
            Predator: [Coordinates(3, 3)],
            Grass: [Coordinates(4, 4), Coordinates(2, 3)],
            Stone: [Coordinates(1, 2)]
        }
        
        # Размещаем сущности
        for entity_class, coords_list in entities.items():
            for coords in coords_list:
                try:
                    self.board.place_entity(coords, entity_class(coords))
                except ValueError as e:
                    self.fail(f"Не удалось разместить {entity_class.__name__} на {coords}: {str(e)}")
        
        # Проверяем количество каждого типа
        for entity_class, coords_list in entities.items():
            entities_of_type = self.board.get_entities_by_type(entity_class)
            self.assertEqual(
                len(entities_of_type),
                len(coords_list),
                f"Неверное количество сущностей типа {entity_class.__name__}: "
                f"ожидалось {len(coords_list)}, получено {len(entities_of_type)}"
            )
            
            # Проверяем, что все сущности правильного типа
            for entity in entities_of_type:
                self.assertIsInstance(
                    entity,
                    entity_class,
                    f"Сущность {entity} не является экземпляром {entity_class.__name__}"
                )
        
    def test_clear_board(self):
        """Тест очистки доски."""
        # Размещаем несколько сущностей
        entities = [
            Herbivore(Coordinates(1, 1)),
            Predator(Coordinates(2, 2)),
            Grass(Coordinates(3, 3))
        ]
        
        for entity in entities:
            self.board.place_entity(entity.coordinates, entity)
        
        # Проверяем, что сущности размещены
        self.assertEqual(len(self.board.entities), len(entities))
        
        # Очищаем доску
        self.board.clear()
        
        # Проверяем, что доска пуста
        self.assertEqual(len(self.board.entities), 0)
        
    def test_move_entity(self):
        """Тест перемещения сущности."""
        # Размещаем сущность
        start_coords = Coordinates(1, 1)
        end_coords = Coordinates(2, 2)
        entity = Herbivore(start_coords)
        self.board.place_entity(start_coords, entity)
        
        # Проверяем успешное перемещение
        self.board.move_entity(start_coords, end_coords)
        self.assertNotIn(start_coords, self.board.entities)
        self.assertIn(end_coords, self.board.entities)
        self.assertEqual(entity.coordinates, end_coords)

    def test_move_entity_invalid_coordinates(self):
        """Тест перемещения сущности на невалидные координаты."""
        # Размещаем сущность
        start_coords = Coordinates(1, 1)
        entity = Herbivore(start_coords)
        self.board.place_entity(start_coords, entity)
        
        invalid_coords = [
            Coordinates(0, 1),    # x < 1
            Coordinates(6, 1),    # x > width
            Coordinates(1, 0),    # y < 1
            Coordinates(1, 6),    # y > height
        ]
        
        for coords in invalid_coords:
            with self.assertRaises(ValueError) as context:
                self.board.move_entity(start_coords, coords)
            self.assertIn(
                "невалидные координаты",
                str(context.exception).lower(),
                f"Неверное сообщение об ошибке для координат {coords}"
            )
            # Проверяем, что сущность осталась на месте
            self.assertEqual(entity.coordinates, start_coords)

    def test_move_entity_to_occupied_cell(self):
        """Тест перемещения сущности на занятую клетку."""
        # Размещаем две сущности
        start_coords = Coordinates(1, 1)
        occupied_coords = Coordinates(2, 2)
        entity1 = Herbivore(start_coords)
        entity2 = Predator(occupied_coords)
        
        self.board.place_entity(start_coords, entity1)
        self.board.place_entity(occupied_coords, entity2)
        
        with self.assertRaises(ValueError) as context:
            self.board.move_entity(start_coords, occupied_coords)
        self.assertIn("уже занята", str(context.exception))
        
        # Проверяем, что сущности остались на своих местах
        self.assertEqual(entity1.coordinates, start_coords)
        self.assertEqual(entity2.coordinates, occupied_coords)