from ..actions.Action import Action
from ..entities.Herbivore import Herbivore
from ..entities.Predator import Predator


class MoveAction(Action):
    def execute(self, board):
        """Перемещение всех существ на поле."""
        print("Перемещение существ...")
        # Создаем копию списка сущностей перед итерацией
        entities = list(board.entities.values())
        for entity in entities:
            if isinstance(entity, (Herbivore, Predator)):
                old_coords = entity.coordinates
                entity.make_move(board)
                if old_coords != entity.coordinates:
                    print(f"{entity} переместился с {old_coords} на {entity.coordinates}")
