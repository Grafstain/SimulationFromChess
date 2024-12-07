from ..core import Coordinates
from ..entities.Creature import Creature
from ..entities.Grass import Grass
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

    def __repr__(self):
        return f"Herbivore"

    def eat(self, food):
        """Восстановление HP при поедании травы."""
        self.hp = min(CREATURE_CONFIG['herbivore']['initial_hp'],
                     self.hp + self.food_value)
        print(f"{self} съел {food} и восстановил {self.food_value} HP. Текущее HP: {self.hp}")

