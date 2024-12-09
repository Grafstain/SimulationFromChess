from ..core import coordinates
from ..entities.creature import Creature
from ..entities.grass import Grass
from ..config import CREATURE_CONFIG


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
        self.max_hp = config['initial_hp']

    def __repr__(self):
        return "Herbivore"

    def interact_with_target(self, board, target):
        """Поедание травы травоядным."""
        if isinstance(target, self.target_type):
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + self.food_value)
            healed = self.hp - old_hp
            board.remove_piece(target.coordinates)
            actions = []
            if healed > 0:
                actions.append(("Съел", f"траву на ({target.coordinates.x}, {target.coordinates.y})"))
            return True, actions
        return False, []

