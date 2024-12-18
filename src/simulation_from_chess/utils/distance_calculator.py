from ..core.coordinates import Coordinates

class DistanceCalculator:
    @staticmethod
    def manhattan_distance(coord1: Coordinates, coord2: Coordinates) -> int:
        """Вычисление манхэттенского расстояния между двумя точками."""
        return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)
    
    @staticmethod
    def is_adjacent(coord1: Coordinates, coord2: Coordinates) -> bool:
        """Проверка, являются ли координаты соседними."""
        return DistanceCalculator.manhattan_distance(coord1, coord2) <= 1 