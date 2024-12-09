from random import randint
from ..actions.action import Action
from ..entities import *
from ..core.coordinates import Coordinates


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
        attempts = 0
        max_attempts = board.width * board.height  # Максимальное количество попыток
        
        for _ in range(count):
            attempts = 0
            while attempts < max_attempts:
                x = randint(1, board.width)  # Изменено с 0 на 1
                y = randint(1, board.height)  # Изменено с 0 на 1
                coords = Coordinates(x, y)
                if board.is_square_empty(coords):
                    board.set_piece(coords, entity_class(coords))
                    break
                attempts += 1
            
            if attempts >= max_attempts:
                print(f"Не удалось разместить {entity_name} после {max_attempts} попыток")

    def __repr__(self):
        return (f"InitAction(herbivores={self.initial_herbivores}, "
                f"predators={self.initial_predators}, "
                f"grass={self.initial_grass}, "
                f"stones={self.initial_stones})")
