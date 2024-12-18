from typing import Dict, Optional, List, Type, Tuple, Set

from .board_state import BoardState
from .coordinates import Coordinates
from .interfaces import IBoard
from .path_finder import PathFinder
from ..entities.entity import Entity  # Базовый класс вместо конкретных
from ..utils.distance_calculator import DistanceCalculator

class Board:
    def __init__(self, width: int, height: int):
        """
        Инициализация игровой доски.
        
        Args:
            width: Ширина поля
            height: Высота поля
            
        Raises:
            ValueError: Если размеры поля невалидны
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"Размеры поля должны быть положительными числами, получено: {width}x{height}")
            
        self.width = width
        self.height = height
        self.entities: Dict[Coordinates, Entity] = {}
        self.game_state = BoardState()
        self.path_finder = PathFinder(self)
        self._entity_cache: Dict[Type[Entity], List[Entity]] = {}

    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """
        Проверка валидности координат.
        
        Args:
            coordinates: Проверяемые координаты
            
        Returns:
            bool: True если координаты валидны, False в противном случае
        """
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)
                
    def place_entity(self, coordinates: Coordinates, entity: Entity) -> None:
        """
        Размещение сущности на доске.
        
        Args:
            coordinates: Координаты для размещения
            entity: Размещаемая сущность
            
        Raises:
            ValueError: Если координаты невалидны или позиция занята
        """
        if not self.is_valid_coordinates(coordinates):
            raise ValueError(f"Невалидные координаты: ({coordinates.x}, {coordinates.y})")
            
        if coordinates in self.entities:
            raise ValueError(f"Позиция ({coordinates.x}, {coordinates.y}) уже занята")
            
        self.entities[coordinates] = entity
        entity.coordinates = coordinates
        self._invalidate_cache()

    def move_entity(self, old_coordinates: Coordinates, new_coordinates: Coordinates) -> None:
        """
        Перемещение сущности с одних координат на другие.
        
        Args:
            old_coordinates: Текущие координаты сущности
            new_coordinates: Новые координаты для перемещения
            
        Raises:
            ValueError: Если координаты невалидны или позиция занята
        """
        if not self.is_valid_coordinates(new_coordinates):
            raise ValueError(f"Невалидные координаты: ({new_coordinates.x}, {new_coordinates.y})")
            
        if old_coordinates not in self.entities:
            raise ValueError(f"На позиции ({old_coordinates.x}, {old_coordinates.y}) нет сущности")
            
        if new_coordinates in self.entities:
            raise ValueError(f"Позиция ({new_coordinates.x}, {new_coordinates.y}) уже занята")
            
        entity = self.entities[old_coordinates]
        del self.entities[old_coordinates]
        self.entities[new_coordinates] = entity
        entity.coordinates = new_coordinates
        self._invalidate_cache()
        
    def get_entities_in_range(self, coordinates: Coordinates, range_limit: int) -> List[Tuple[Entity, int]]:
        """Получение списка сущностей в радиусе."""
        return self.path_finder.get_entities_in_range(coordinates, range_limit)
        
    def find_path(self, start: Coordinates, end: Coordinates) -> Optional[List[Coordinates]]:
        """Поиск пути между двумя точками."""
        return self.path_finder.find_path(start, end)
        
    def get_entities_by_type(self, entity_type: Type) -> List[Entity]:
        """Получение всех сущностей определенного типа."""
        return [
            entity for entity in self.entities.values()
            if isinstance(entity, entity_type)
        ]
    
    def get_entities_in_radius(self, center: Coordinates, radius: int) -> List[Entity]:
        """Получение всех сущностей в заданном радиусе."""
        return [
            entity for entity in self.entities.values()
            if DistanceCalculator.manhattan_distance(center, entity.coordinates) <= radius
        ]
    
    def clear_caches(self) -> None:
        """Очистка всех кэшей."""
        self.path_finder._path_cache.clear()
        self.path_finder._available_moves_cache.clear()

    def _invalidate_cache(self) -> None:
        """Инвалидация кэша сущностей."""
        self._entity_cache.clear()
        
    def get_empty_cells(self) -> List[Coordinates]:
        """Получение списка пустых клеток."""
        empty_cells = []
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                coords = Coordinates(x, y)
                if coords not in self.entities:
                    empty_cells.append(coords)
        return empty_cells

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

    def is_within_bounds(self, coordinates: Coordinates) -> bool:
        """
        Проверяет, находятся ли координаты в пределах доски.
        
        Args:
            coordinates: Проверяемые коо��динаты
            
        Returns:
            bool: True если координаты в пределах доски, False иначе
        """
        return (1 <= coordinates.x <= self.width and 
                1 <= coordinates.y <= self.height)

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

    def clear(self) -> None:
        """Очистка доски от всех сущностей."""
        self.entities.clear()
        self._invalidate_cache()
