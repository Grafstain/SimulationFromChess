from ..core.coordinates import Coordinates
from ..entities.creature import Creature
from ..entities.grass import Grass
from ..config import CREATURE_CONFIG
from typing import Tuple, Optional


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
        """Поиск ближайшей травы."""
        entities_in_range = board.get_entities_in_range(self.coordinates, self.speed * 2)
        
        # Фильтруем только траву
        grass_targets = [
            (entity, distance) for entity, distance in entities_in_range
            if isinstance(entity, Grass)
        ]
        
        # Возвращаем ближайшую траву или None, если травы нет
        return grass_targets[0][0] if grass_targets else None

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

