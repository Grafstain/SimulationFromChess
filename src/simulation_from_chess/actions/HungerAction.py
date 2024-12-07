from ..actions.Action import Action
from ..entities.Creature import Creature


class HungerAction(Action):
    def __init__(self, hunger_damage=1):
        self.hunger_damage = hunger_damage

    def execute(self, board):
        """Наносит урон от голода всем существам на поле."""
        print("Checking hunger...")
        for entity in board.entities.values():
            if isinstance(entity, Creature):
                entity.take_damage(self.hunger_damage) 