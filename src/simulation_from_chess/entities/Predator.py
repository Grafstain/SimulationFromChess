from ..core import Coordinates
from ..entities.Herbivore import Herbivore
from ..entities.Creature import Creature
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

    def __repr__(self):
        return f"Predator"

    def attack(self, target):
        """Атака цели."""
        target.take_damage(self.attack_damage)
        if target.hp <= 0:
            self.hp = min(CREATURE_CONFIG['predator']['initial_hp'],
                         self.hp + self.food_value)
            print(f"{self} съел {target} и восстановил {self.food_value} HP. Текущее HP: {self.hp}")



