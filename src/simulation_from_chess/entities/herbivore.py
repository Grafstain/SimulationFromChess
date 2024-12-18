from ..core.coordinates import Coordinates
from ..entities.creature import Creature
from ..entities.grass import Grass
from ..config import CREATURE_CONFIG
from typing import Tuple, Optional

from ..utils.distance_calculator import DistanceCalculator


class Herbivore(Creature):
    def __init__(self, coordinates: Coordinates):
        config = CREATURE_CONFIG['herbivore']
        super().__init__(
            coordinates=coordinates,
            speed=config['speed'],
            hp=config['initial_hp']
        )
        self.target_type = Grass
        self.food_value = config['food_value']

    def __repr__(self):
        """Строковое представление травоядного."""
        return "Травоядный"

    def interact_with_target(self, board, target):
        """Поедание травы травоядным."""
        if isinstance(target, self.target_type):
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + self.food_value)
            healed = self.hp - old_hp
            board.remove_entity(target.coordinates)
            actions = []
            if healed > 0:
                actions.append(("Съел", f"траву на ({target.coordinates.x}, {target.coordinates.y})"))
            return True, actions
        return False, []

    def _get_planned_interaction(self, target) -> Tuple[str, str]:
        """Описание планируемого поедания травы."""
        return ("Планирует съесть", f"траву на ({target.coordinates.x}, {target.coordinates.y})")

    def needs_food(self) -> bool:
        """Проверка, нужна ли еда существу."""
        return self.hp < self.max_hp

    def find_target(self, board):
        """
        Поиск ближайшей травы.
        
        Args:
            board: Игровая доска
            
        Returns:
            Optional[Entity]: Найденная трава или None
        """
        # Получаем все сущности типа Grass на поле
        grass_targets = [
            (entity, DistanceCalculator.manhattan_distance(self.coordinates, entity.coordinates))
            for entity in board.get_entities_by_type(Grass)
        ]
        
        # Сортируем по расстоянию и возвращаем ближайшую траву
        if grass_targets:
            grass_targets.sort(key=lambda x: x[1])
            return grass_targets[0][0]
        return None

    def _find_best_move(self, target_coords: Coordinates) -> Optional[Coordinates]:
        """Находит лучший ход в направлении цели."""
        if not self.available_moves:
            return None
        
        # Сортируем доступные ходы по расстоянию до цели
        moves_with_distances = [
            (move, abs(move.x - target_coords.x) + abs(move.y - target_coords.y))
            for move in self.available_moves
        ]
        moves_with_distances.sort(key=lambda x: x[1])
        
        return moves_with_distances[0][0] if moves_with_distances else None

