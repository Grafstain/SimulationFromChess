from ..actions import *
from ..entities import Herbivore, Predator


class MoveAction(Action):
    def execute(self, board):
        print("Moving entities...")
        for entity in board.entities.values():
            if isinstance(entity, (Herbivore, Predator)):
                entity.make_move(board)  # Предполагается, что у сущностей есть метод make_move()
