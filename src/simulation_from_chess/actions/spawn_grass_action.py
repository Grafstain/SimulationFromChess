from random import randint
from typing import List

from ..core.coordinates import Coordinates
from ..entities.grass import Grass
from .action import Action


class SpawnGrassAction(Action):
    def __init__(self, min_grass: int = 3, spawn_chance: float = 0.3):
        """
        Инициализация действия спавна травы.
        
        Args:
            min_grass: Минимальное количество травы на поле
            spawn_chance: Шанс появления новой травы (0.0 - 1.0)
        """
        self.min_grass = min_grass
        self.spawn_chance = spawn_chance

    def execute(self, board, logger) -> None:
        """
        Добавляет траву на поле, если её слишком мало.
        
        Args:
            board: Игровая доска
            logger: Логгер для записи действий
        """
        grass_count = self._count_grass(board)
        
        if grass_count < self.min_grass and self._should_spawn():
            empty_coords = self._find_empty_positions(board)
            
            if empty_coords:
                spawn_pos = empty_coords[randint(0, len(empty_coords) - 1)]
                grass = Grass(spawn_pos)
                if board.place_entity(spawn_pos, grass):
                    logger.log_action(grass, "Появилась", f"на координатах ({spawn_pos.x}, {spawn_pos.y})")

    def _count_grass(self, board) -> int:
        """Подсчет количества травы на поле."""
        return sum(1 for entity in board.entities.values() 
                  if isinstance(entity, Grass))

    def _should_spawn(self) -> bool:
        """Проверка, должна ли появиться новая трава."""
        return randint(1, 100) / 100 <= self.spawn_chance

    def _find_empty_positions(self, board) -> List[Coordinates]:
        """Поиск пустых позиций на поле."""
        return [
            Coordinates(x, y)
            for x in range(1, board.width + 1)  # Изменено с 0 на 1
            for y in range(1, board.height + 1)  # Изменено с 0 на 1
            if board.is_position_vacant(Coordinates(x, y))
        ]

    def __repr__(self) -> str:
        """Строковое представление действия."""
        return f"SpawnGrassAction(min_grass={self.min_grass}, spawn_chance={self.spawn_chance})" 