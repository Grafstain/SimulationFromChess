from ..actions.action import Action
from ..entities.creature import Creature
from ..core.board import Board
from ..utils.logger import Logger


class HungerAction(Action):
    def __init__(self, hunger_damage: int):
        self.hunger_damage = hunger_damage

    def execute(self, board: Board, logger: Logger) -> None:
        """
        Применяет урон от голода ко всем существам.
        
        Args:
            board: Игровое поле
            logger: Логгер (не используется для голода)
        """
        for entity in board.entities.values():
            if isinstance(entity, Creature):
                entity.take_damage(self.hunger_damage)