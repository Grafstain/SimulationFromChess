import random
from typing import Dict

from ..core.coordinates import Coordinates
from ..entities import *
from src.simulation_from_chess.utils.Logger import Logger


class Board:
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.entities: Dict[Coordinates, Entity] = {}

    def place_entity(self, coordinates: Coordinates, entity: Entity):
        """Размещение сущности на поле с проверкой границ."""
        if not self.is_within_bounds(coordinates) or not self.is_position_vacant(coordinates):
            return False
        entity.coordinates = coordinates
        self.entities[coordinates] = entity
        return True

    def remove_entity(self, coordinates: Coordinates):
        """Удаление сущности с поля."""
        if coordinates in self.entities:
            del self.entities[coordinates]

    def is_position_vacant(self, coordinates: Coordinates) -> bool:
        """Проверка свободна ли позиция."""
        if not self.is_within_bounds(coordinates):
            return False
        return coordinates not in self.entities

    def get_entity(self, coordinates: Coordinates) -> Entity:
        """Получение сущности с проверкой валидности координат."""
        if not self.is_within_bounds(coordinates):
            return None
        return self.entities.get(coordinates)

    def move_entity(self, old_coords: Coordinates, new_coords: Coordinates) -> bool:
        """
        Перемещение сущности с одной позиции на другую.
        
        Args:
            old_coords (Coordinates): Текущие координаты
            new_coords (Coordinates): Новые координаты
        Returns:
            bool: True если перемещение успешно, False если нет
        """
        if not self.is_within_bounds(old_coords) or not self.is_within_bounds(new_coords):
            return False
            
        entity = self.entities.get(old_coords)
        if entity is None:
            return False
            
        # Удаляем сущность со старой позиции
        del self.entities[old_coords]
        
        # Помещаем сущность на новую позицию
        self.entities[new_coords] = entity
        
        return True

    def is_within_bounds(self, coordinates: Coordinates) -> bool:
        """Проверка находятся ли координаты в пределах поля."""
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)
