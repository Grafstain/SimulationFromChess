from random import randint
from typing import Type, Dict

from ..actions.action import Action
from ..entities.entity import Entity
from ..entities.herbivore import Herbivore
from ..entities.predator import Predator
from ..entities.grass import Grass
from ..entities.stone import Stone
from ..core.coordinates import Coordinates


class InitAction(Action):
    def __init__(self, herbivores: int = 3, predators: int = 2, grass: int = 5, stones: int = 3):
        """
        Инициализация начальных параметров симуляции.
        
        Args:
            herbivores: Количество травоядных
            predators: Количество хищников
            grass: Количество травы
            stones: Количество камней
        """
        self.initial_entities: Dict[Type[Entity], int] = {
            Herbivore: herbivores,
            Predator: predators,
            Grass: grass,
            Stone: stones
        }

    def execute(self, board, logger):
        """Инициализация доски начальными сущностями."""
        for entity_class, count in self.initial_entities.items():
            self._place_entities(board, entity_class, count)

    def _place_entities(self, board, entity_class: Type[Entity], count: int) -> None:
        """
        Размещение сущностей определенного типа на доске.
        
        Args:
            board: Игровая доска
            entity_class: Класс размещаемой сущности
            count: Количество сущностей для размещения
        """
        entity_name = entity_class.__name__.lower()
        max_attempts = board.width * board.height
        placed_count = 0
        
        while placed_count < count:
            for _ in range(max_attempts):
                coords = self._generate_random_coordinates(board)
                if board.is_position_vacant(coords):
                    entity = entity_class(coords)
                    if board.place_entity(coords, entity):
                        placed_count += 1
                        break
            else:  # Если не удалось разместить после всех попыток
                logger.log_action(
                    None,
                    "Ошибка размещения",
                    f"Не удалось разместить {entity_name} после {max_attempts} попыток"
                )
                break

    @staticmethod
    def _generate_random_coordinates(board) -> Coordinates:
        """
        Генерация случайных координат в пределах доски.
        
        Args:
            board: Игровая доска
        Returns:
            Coordinates: Случайные координаты
        """
        x = randint(1, board.width)
        y = randint(1, board.height)
        return Coordinates(x, y)

    def __repr__(self) -> str:
        """Строковое представление действия."""
        return (f"InitAction("
                f"herbivores={self.initial_entities[Herbivore]}, "
                f"predators={self.initial_entities[Predator]}, "
                f"grass={self.initial_entities[Grass]}, "
                f"stones={self.initial_entities[Stone]})")
