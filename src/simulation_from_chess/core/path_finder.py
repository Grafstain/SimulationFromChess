import heapq
from typing import List, Optional, Set, Tuple
from .coordinates import Coordinates
from .interfaces import IBoard
from ..entities import Entity
from ..utils.distance_calculator import DistanceCalculator


class PathFinder:
    def __init__(self, board: IBoard):
        self.board = board
        self._path_cache = {}
        self._available_moves_cache = {}
        
    def find_path(self, start: Coordinates, end: Coordinates, max_distance: int = None) -> Optional[List[Coordinates]]:
        """
        Поиск пути между двумя точками используя A*.
        
        Args:
            start: Начальные координаты
            end: Конечные координаты
            max_distance: Максимальная длина пути
        """
        cache_key = (start, end, max_distance)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]
            
        path = self._a_star(start, end, max_distance)
        self._path_cache[cache_key] = path
        return path
    
    def get_available_moves(self, coordinates: Coordinates, speed: int) -> Set[Coordinates]:
        """
        Получение доступных ходов с учетом скорости.
        
        Args:
            coordinates: Текущие координаты
            speed: Скорость существа (максимальное расстояние перемещения)
        
        Returns:
            Set[Coordinates]: Множество доступных координат для перемещения
        """
        cache_key = (coordinates, speed)
        if cache_key in self._available_moves_cache:
            return self._available_moves_cache[cache_key]
            
        moves = set()
        for dx in range(-speed, speed + 1):
            for dy in range(-speed + abs(dx), speed - abs(dx) + 1):
                new_coords = Coordinates(coordinates.x + dx, coordinates.y + dy)
                if (self.board.is_valid_coordinates(new_coords) and 
                    self.board.is_position_vacant(new_coords)):
                    moves.add(new_coords)
        
        self._available_moves_cache[cache_key] = moves
        return moves
    
    def find_nearest_target(self, start: Coordinates, target_type: type, max_distance: int = None) -> Optional[Tuple[Entity, List[Coordinates]]]:
        """Поиск ближайшей цели определенного типа."""
        nearest_target = None
        best_path = None
        min_distance = float('inf')
        
        for entity in self.board.get_entities_by_type(target_type):
            distance = DistanceCalculator.manhattan_distance(start, entity.coordinates)
            if distance < min_distance:
                path = self.find_path(start, entity.coordinates, max_distance)
                if path:
                    min_distance = distance
                    nearest_target = entity
                    best_path = path
                    
        return (nearest_target, best_path) if nearest_target else None
    
    def _a_star(self, start: Coordinates, end: Coordinates, max_distance: int = None) -> Optional[List[Coordinates]]:
        """
        Реализация алгоритма A*.
        """
        def heuristic(coords: Coordinates) -> int:
            return DistanceCalculator.manhattan_distance(coords, end)
        
        # Используем id для уникальной идентификации элементов в куче
        counter = 0
        open_set = [(0, counter, start)]
        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            current_f, _, current = heapq.heappop(open_set)
            
            if current == end:
                path = self._reconstruct_path(came_from, current)
                if max_distance is None or len(path) <= max_distance:
                    return path
                return None
            
            if max_distance and g_score[current] >= max_distance:
                continue
                
            for next_pos in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if next_pos not in g_score or tentative_g < g_score[next_pos]:
                    came_from[next_pos] = current
                    g_score[next_pos] = tentative_g
                    f_score = tentative_g + heuristic(next_pos)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, next_pos))
        
        return None
    
    def _get_neighbors(self, coords: Coordinates) -> List[Coordinates]:
        """
        Получение соседних координат.
        
        Args:
            coords: Текущие координаты
            
        Returns:
            List[Coordinates]: Список доступных соседних координат
        """
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_coords = Coordinates(coords.x + dx, coords.y + dy)
            if (self.board.is_valid_coordinates(new_coords) and 
                not self.board.get_entity(new_coords)):
                neighbors.append(new_coords)
        return neighbors
    
    def _reconstruct_path(self, came_from: dict, current: Coordinates) -> List[Coordinates]:
        """Восстановление пути из came_from словаря."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]