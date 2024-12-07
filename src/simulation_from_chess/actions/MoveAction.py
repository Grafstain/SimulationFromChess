from ..actions.Action import Action
from ..entities.Herbivore import Herbivore
from ..entities.Predator import Predator


class MoveAction(Action):
    def execute(self, board):
        print("Moving entities...")
        # Создаем копию списка сущностей перед итерацией
        entities = list(board.entities.values())
        for entity in entities:
            if isinstance(entity, (Herbivore, Predator)):
                entity.make_move(board)
