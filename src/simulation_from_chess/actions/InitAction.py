from random import randint
from ..actions.Action import Action
from ..entities import Herbivore, Predator, Grass
from ..core.Coordinates import Coordinates


class InitAction(Action):
    def __init__(self, herbivores=3, predators=2, grass=5):
        self.initial_herbivores = herbivores
        self.initial_predators = predators
        self.initial_grass = grass

    def execute(self, board):
        """Инициализация доски начальными сущностями."""
        print("Initializing board with entities...")
        
        # Размещаем травоядных
        for _ in range(self.initial_herbivores):
            while True:
                x = randint(0, board.width - 1)
                y = randint(0, board.height - 1)
                coords = Coordinates(x, y)
                if board.is_square_empty(coords):
                    board.set_piece(coords, Herbivore(coords))
                    break

        # Размещаем хищников
        for _ in range(self.initial_predators):
            while True:
                x = randint(0, board.width - 1)
                y = randint(0, board.height - 1)
                coords = Coordinates(x, y)
                if board.is_square_empty(coords):
                    board.set_piece(coords, Predator(coords))
                    break

        # Размещаем траву
        for _ in range(self.initial_grass):
            while True:
                x = randint(0, board.width - 1)
                y = randint(0, board.height - 1)
                coords = Coordinates(x, y)
                if board.is_square_empty(coords):
                    board.set_piece(coords, Grass(coords))
                    break

    def __repr__(self):
        return (f"InitAction(herbivores={self.initial_herbivores}, "
                f"predators={self.initial_predators}, "
                f"grass={self.initial_grass})")
