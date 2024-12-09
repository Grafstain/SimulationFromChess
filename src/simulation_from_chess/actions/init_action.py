from typing import Type
from ..core.board import Board
from ..entities.entity import Entity
from ..entities.grass import Grass
from ..entities.stone import Stone
from ..entities.herbivore import Herbivore
from ..entities.predator import Predator
from .action import Action
from ..core.coordinates import Coordinates
import random

class InitAction(Action):
    def __init__(self, herbivores: int = 0, predators: int = 0, grass: int = 0, stones: int = 0):
        """
        Инициализация действия.
        
        Args:
            herbivores: Количество травоядных
            predators: Количество хищников
            grass: Количество травы
            stones: Количество камней
        """
        self.entities_to_place = {
            Herbivore: herbivores,
            Predator: predators,
            Grass: grass,
            Stone: stones
        }

    def execute(self, board: Board, logger) -> None:
        """
        Выполнение инициализации - размещение сущностей на доске.
        
        Args:
            board: Игровая доска
            logger: Логгер для записи действий
        """
        for entity_class, count in self.entities_to_place.items():
            if count > 0:
                self._place_entities(board, entity_class, count, logger)

    def _place_entities(self, board: Board, entity_class: Type[Entity], count: int, logger) -> None:
        """
        Размещение сущностей определенного типа на доске.
        
        Args:
            board: Игровая доска
            entity_class: Класс размещаемой сущности
            count: Количество сущностей для размещения
            logger: Логгер для записи действий
        """
        entity_name = entity_class.__name__.lower()
        max_attempts = board.width * board.height
        placed_count = 0

        while placed_count < count:
            for _ in range(max_attempts):
                coords = self._generate_random_coordinates(board)
                if board.is_position_vacant(coords):
                    entity = entity_class(coords)
                    try:
                        board.place_entity(coords, entity)
                        placed_count += 1
                        logger.log_action(
                            None,
                            "Размещение",
                            f"Размещен {entity_name} на координатах ({coords.x}, {coords.y})"
                        )
                        break
                    except ValueError as e:
                        continue
            else:  # Если не удалось разместить после всех попыток
                logger.log_action(
                    None,
                    "Ошибка размещения",
                    f"Не удалось разместить {entity_name} после {max_attempts} попыток"
                )
                break

    def _generate_random_coordinates(self, board: Board) -> Coordinates:
        """
        Генерация случайных координат в пределах доски.
        
        Args:
            board: Игровая доска
            
        Returns:
            Coordinates: Случайные координаты
        """
        return Coordinates(
            random.randint(1, board.width),
            random.randint(1, board.height)
        )

    def __repr__(self) -> str:
        """Строковое представление действия."""
        return (f"InitAction(herbivores={self.entities_to_place[Herbivore]}, "
                f"predators={self.entities_to_place[Predator]}, "
                f"grass={self.entities_to_place[Grass]}, "
                f"stones={self.entities_to_place[Stone]})")
