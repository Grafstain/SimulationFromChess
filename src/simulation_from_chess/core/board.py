import random
from typing import Dict, List

from ..core.coordinates import Coordinates
from ..entities import *
from src.simulation_from_chess.utils.logger import Logger


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

    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """Проверка валидности координат."""
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)

    def place_entity(self, coordinates: Coordinates, entity) -> None:
        """
        Размещение сущности на доске.
        
        Raises:
            ValueError: Если координаты невалидны или позиция занята
        """
        if not self.is_valid_coordinates(coordinates):
            raise ValueError(f"Невалидные координаты: {coordinates}")
            
        if not self.is_position_vacant(coordinates):
            raise ValueError(f"Позиция {coordinates} уже занята")
            
        self.entities[coordinates] = entity

    def remove_entity(self, coordinates: Coordinates) -> bool:
        """
        Удаление сущности с доски.
        
        Returns:
            bool: True если сущность была удалена, False если её не было
        """
        return self.entities.pop(coordinates, None) is not None

    def get_entity(self, coordinates: Coordinates):
        """Получение сущности по координатам."""
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

    def get_entities_by_type(self, entity_type) -> List:
        """Получение списка сущностей определенного типа."""
        return [entity for entity in self.entities.values() 
                if isinstance(entity, entity_type)]

    def clear(self) -> None:
        """Очистка доски."""
        self.entities.clear()

    def move_entity(self, from_coords: Coordinates, to_coords: Coordinates) -> bool:
        """
        Перемещение сущности с одной позиции на другую.
        
        Args:
            from_coords: Исходные координаты
            to_coords: Целевые координаты
            
        Returns:
            bool: True если перемещение успешно, False если нет
            
        Raises:
            ValueError: Если координаты невалидны или целевая позиция занята
        """
        if not self.is_valid_coordinates(to_coords):
            raise ValueError(f"Невалидные целевые координаты: {to_coords}")
            
        if not self.is_position_vacant(to_coords):
            raise ValueError(f"Целевая позиция {to_coords} уже занята")
            
        entity = self.get_entity(from_coords)
        if entity is None:
            return False
            
        self.remove_entity(from_coords)
        self.place_entity(to_coords, entity)
        entity.coordinates = to_coords
        return True

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
