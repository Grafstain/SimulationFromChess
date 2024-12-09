from ..core.coordinates import Coordinates
from ..entities.creature import Creature
from ..entities.herbivore import Herbivore
from ..config import CREATURE_CONFIG


class Predator(Creature):
    def __init__(self, coordinates: Coordinates):
        config = CREATURE_CONFIG['predator']
        super().__init__(
            coordinates=coordinates,
            speed=config['speed'],
            hp=config['initial_hp']
        )
        self.target_type = Herbivore
        self.attack_damage = config['attack_damage']
        self.food_value = config['food_value']
        self.max_hp = config['initial_hp']

    def __repr__(self):
        return "Predator"

    def interact_with_target(self, board, target):
        """Атака травоядного хищником."""
        if isinstance(target, self.target_type):
            target.take_damage(self.attack_damage)
            actions = [("Атаковал", f"травоядного на ({target.coordinates.x}, {target.coordinates.y})")]
            
            if target.hp <= 0:
                old_hp = self.hp
                self.hp = min(self.max_hp, self.hp + self.food_value)
                healed = self.hp - old_hp
                if healed > 0:
                    actions.append(("Съел", f"травоядного на ({target.coordinates.x}, {target.coordinates.y})"))
                board.remove_entity(target.coordinates)
            return True, actions
        return False, []

