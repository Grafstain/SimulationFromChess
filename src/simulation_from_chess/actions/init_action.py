from typing import Type
from ..core.board import Board
from ..entities.creature import Creature
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
        # Сбрасываем счетчики существ перед новой инициализацией
        Creature.reset_counters()
        
        for entity_class, count in self.entities_to_place.items():
            if count > 0:
                self._place_entities(board, entity_class, count, logger)
        
        # Обновляем состояние всех существ после размещения
        logger.log_creatures_state(board.entities)
        
        # Логируем начальное состояние всех существ
        for entity in board.entities.values():
            if isinstance(entity, Creature):
                logger.log_action(
                    entity, 
                    "Создан", 
                    f"на ({entity.coordinates.x}, {entity.coordinates.y}) с {entity.hp}/{entity.max_hp} HP"
                )

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
        
        # Получаем все валидные координаты
        valid_coords = [
            Coordinates(x, y)
            for x in range(1, board.width + 1)
            for y in range(1, board.height + 1)
            if board.is_valid_coordinates(Coordinates(x, y)) and board.is_position_vacant(Coordinates(x, y))
        ]
        
        if len(valid_coords) < count:
            logger.log_action(
                None,
                "Ошибка размещения",
                f"Недостаточно места для размещения {count} {entity_name} (доступно {len(valid_coords)} клеток)"
            )
            count = len(valid_coords)  # Размещаем столько, сколько возможно
        
        # Случайно перемешиваем координаты
        random.shuffle(valid_coords)
        
        # Размещаем сущности на случайных свободных координатах
        placed_count = 0
        for coords in valid_coords[:count]:
            try:
                # Дополнительная проверка валидности координат
                if not (1 <= coords.x <= board.width and 1 <= coords.y <= board.height):
                    logger.log_action(
                        None,
                        "Ошибка размещения",
                        f"Невалидные координаты ({coords.x}, {coords.y})"
                    )
                    continue
                    
                entity = entity_class(coords)
                board.place_entity(coords, entity)
                placed_count += 1
                logger.log_action(
                    None,
                    "Размещение",
                    f"Размещен {entity_name} на координатах ({coords.x}, {coords.y})"
                )
            except ValueError as e:
                logger.log_action(
                    None,
                    "Ошибка размещения",
                    f"Не удалось разместить {entity_name} на координатах ({coords.x}, {coords.y}): {str(e)}"
                )
        
        if placed_count < count:
            logger.log_action(
                None,
                "Предупреждение",
                f"Размещено только {placed_count} из {count} {entity_name}"
            )

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
