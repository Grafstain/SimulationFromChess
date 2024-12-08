from ..actions.Action import Action
from ..entities.Creature import Creature


class HungerAction(Action):
    def __init__(self, hunger_damage=1):
        self.hunger_damage = hunger_damage

    def execute(self, board, logger):
        """Наносит урон от голода всем существам на поле."""
        for entity in board.entities.values():
            if isinstance(entity, Creature):
                entity.take_damage(self.hunger_damage)
                logger.log_action(entity, "Голод", f"-{self.hunger_damage} HP")