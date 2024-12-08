from random import randint
from ..actions.Action import Action
from ..entities import Herbivore, Predator, Grass, Stone
from ..core.Coordinates import Coordinates


class InitAction(Action):
    def __init__(self, herbivores=3, predators=2, grass=5, stones=3):
        self.initial_herbivores = herbivores
        self.initial_predators = predators
        self.initial_grass = grass
        self.initial_stones = stones

    def execute(self, board, logger):
        """Инициализация доски начальными сущностями."""
        self._place_entities(board, Herbivore, self.initial_herbivores)
        self._place_entities(board, Predator, self.initial_predators)
        self._place_entities(board, Grass, self.initial_grass)
        self._place_entities(board, Stone, self.initial_stones)

    def _place_entities(self, board, entity_class, count):
        """Вспомогательный метод для размещения сущностей на доске."""
        entity_name = entity_class.__name__.lower()
        for _ in range(count):
            while True:
                x = randint(0, board.width - 1)
                y = randint(0, board.height - 1)
                coords = Coordinates(x, y)
                if board.is_square_empty(coords):
                    board.set_piece(coords, entity_class(coords))
                    break

    def __repr__(self):
        return (f"InitAction(herbivores={self.initial_herbivores}, "
                f"predators={self.initial_predators}, "
                f"grass={self.initial_grass}, "
                f"stones={self.initial_stones})")
