import random
from typing import Dict, List, Optional, Type

from ..core.coordinates import Coordinates
from ..entities import *
from src.simulation_from_chess.utils.logger import Logger
from src.simulation_from_chess.core.game_state import GameState


class Board:
    def __init__(self, width: int, height: int):
        """
        Инициализация игровой доски.
        
        Args:
            width: Ширина доски
            height: Высота доски
            
        Raises:
            ValueError: Если размеры доски невалидны
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Размеры доски должны быть положительными числами, получено: width={width}, height={height}")
            
        self.width = width
        self.height = height
        self.entities = {}
        self.game_state = GameState()

    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """Проверка валидности координат."""
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)

    def place_entity(self, coordinates: Coordinates, entity: Entity) -> None:
        """
        Размещает сущность на доске.
        
        Args:
            coordinates: Координаты для размещения
            entity: Размещаемая сущность
            
        Raises:
            ValueError: Если клетка уже занята или координаты вне поля
        """
        if coordinates in self.entities:
            raise ValueError(f"Клетка {coordinates} уже занята")
        
        if not (1 <= coordinates.x <= self.width and 1 <= coordinates.y <= self.height):
            raise ValueError(f"Координаты {coordinates} находятся вне поля")
        
        self.entities[coordinates] = entity
        entity.coordinates = coordinates

    def remove_entity(self, coordinates: Coordinates) -> None:
        """
        Удалить сущность с указанных координат.
        
        Args:
            coordinates: Координаты для удаления
        """
        if coordinates in self.entities:
            del self.entities[coordinates]

    def get_entity(self, coordinates: Coordinates) -> Optional[Entity]:
        """
        Получить сущность по координатам.
        
        Args:
            coordinates: Координаты для поиска
        
        Returns:
            Optional[Entity]: Сущность, если она есть на указанных координатах, иначе None
        """
        return self.entities.get(coordinates)

    def is_position_vacant(self, coordinates: Coordinates) -> bool:
        """Проверка, свободна ли позиция."""
        return coordinates not in self.entities

    def get_adjacent_positions(self, coordinates: Coordinates) -> List[Coordinates]:
        """Получение списка соседних позиций."""
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                new_coords = Coordinates(coordinates.x + dx, coordinates.y + dy)
                if self.is_valid_coordinates(new_coords):
                    adjacent.append(new_coords)
                    
        return adjacent

    def get_entities_by_type(self, entity_type: Type) -> List[Entity]:
        """
        Получить список всех сущностей указанного типа.
        
        Args:
            entity_type: Тип искомых сущностей
        
        Returns:
            List[Entity]: Список сущностей указанного типа
        """
        return [
            entity for entity in self.entities.values() 
            if isinstance(entity, entity_type)
        ]

    def clear(self) -> None:
        """Очистка доски."""
        self.entities.clear()

    def move_entity(self, entity: Entity, new_coordinates: Coordinates) -> None:
        """
        Перемещает сущность на новые координаты.
        
        Args:
            entity: Перемещаемая сущность
            new_coordinates: Новые координаты
        
        Raises:
            ValueError: Если новые координаты заняты или находятся вне поля
        """
        if new_coordinates in self.entities:
            raise ValueError(f"Клетка {new_coordinates} уже занята")
        
        if not (1 <= new_coordinates.x <= self.width and 
                1 <= new_coordinates.y <= self.height):
            raise ValueError(f"Координаты {new_coordinates} находятся вне поля")
        
        # Удаляем сущность со старых координат
        old_coordinates = entity.coordinates
        if old_coordinates in self.entities:
            del self.entities[old_coordinates]
        
        # Размещаем на новых координатах
        self.entities[new_coordinates] = entity
        entity.coordinates = new_coordinates

    def get_vacant_adjacent_positions(self, coordinates: Coordinates) -> List[Coordinates]:
        """Получение списка свободных соседних позиций."""
        return [pos for pos in self.get_adjacent_positions(coordinates) 
                if self.is_position_vacant(pos)]

    def get_entities_in_range(self, coordinates: Coordinates, range_limit: int) -> List[tuple]:
        """
        Получение списка сущностей в заданном радиусе.
        
        Args:
            coordinates: Центральные координаты
            range_limit: Максимальное расстояние
            
        Returns:
            List[tuple]: Список кортежей (сущность, расстояние)
        """
        entities_in_range = []
        for entity_coords, entity in self.entities.items():
            if entity_coords == coordinates:
                continue
                
            distance = self._calculate_distance(coordinates, entity_coords)
            if distance <= range_limit:
                entities_in_range.append((entity, distance))
                
        return sorted(entities_in_range, key=lambda x: x[1])

    def _calculate_distance(self, coords1: Coordinates, coords2: Coordinates) -> int:
        """Вычисление манхэттенского расстояния между координатами."""
        return abs(coords1.x - coords2.x) + abs(coords1.y - coords2.y)

    def next_turn(self) -> None:
        """Переход к следующему ходу."""
        self.game_state.current_turn += 1
        # Сохраняем состояние всех сущностей
        for entity in self.entities.values():
            self.game_state.save_entity_state(
                self.game_state.current_turn,
                entity.entity_id,
                entity.get_state()
            )

    def update_entity_state(self, entity: Entity) -> None:
        """Обновление состояния сущности."""
        self.game_state.save_entity_state(
            self.game_state.current_turn,
            entity.entity_id,
            entity.get_state()
        )

    def get_empty_cells(self) -> List[Coordinates]:
        """
        Получить список пустых клеток на доске.
        
        Returns:
            List[Coordinates]: Список координат пустых клеток
        """
        empty_cells = []
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                coords = Coordinates(x, y)
                if coords not in self.entities:
                    empty_cells.append(coords)
        return empty_cells

    def manhattan_distance(self, coords1: Coordinates, coords2: Coordinates) -> int:
        """
        Вычисляет манхэттенское расстояние между двумя точками.
        
        Args:
            coords1: Первая точка
            coords2: Вторая точка
            
        Returns:
            int: Манхэттенское расстояние
        """
        return abs(coords1.x - coords2.x) + abs(coords1.y - coords2.y)
