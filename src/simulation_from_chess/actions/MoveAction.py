from ..actions.Action import Action
from ..entities.Herbivore import Herbivore
from ..entities.Predator import Predator


class MoveAction(Action):
    def execute(self, board, logger):
        """Перемещение всех существ на поле."""
        entities = list(board.entities.values())
        for entity in entities:
            if isinstance(entity, (Herbivore, Predator)):
                actions = entity.make_move(board)
                for action in actions:
                    if isinstance(action, tuple) and len(action) == 2:
                        logger.log_action(entity, action[0], action[1])
