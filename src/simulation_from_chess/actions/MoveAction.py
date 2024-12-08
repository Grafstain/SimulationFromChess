from ..actions.Action import Action
from ..entities.Herbivore import Herbivore
from ..entities.Predator import Predator


class MoveAction(Action):
    def execute(self, board, logger):
        """Перемещение всех существ на поле."""
        entities = list(board.entities.values())
        for entity in entities:
            if isinstance(entity, (Herbivore, Predator)):
                old_coords = entity.coordinates
                entity.make_move(board)
                if old_coords != entity.coordinates:
                    logger.log_action(entity, "Перемещение", 
                        f"с ({old_coords.x}, {old_coords.y}) на ({entity.coordinates.x}, {entity.coordinates.y})")
