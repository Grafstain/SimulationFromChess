from typing import List, Tuple, Union

from ..actions.action import Action
from ..entities.herbivore import Herbivore
from ..entities.predator import Predator
from ..entities.creature import Creature


class MoveAction(Action):
    def execute(self, board, logger) -> None:
        """
        Перемещение всех существ на поле.
        
        Args:
            board: Игровая доска
            logger: Логгер для записи действий
        """
        # Создаем копию списка существ, чтобы избежать проблем с изменением словаря во время итерации
        entities = [
            entity for entity in board.entities.values()
            if isinstance(entity, (Herbivore, Predator))
        ]
        
        for entity in entities:
            self._process_creature_move(entity, board, logger)

    def _process_creature_move(self, creature: Creature, board, logger) -> None:
        """
        Обработка перемещения одного существа.
        
        Args:
            creature: Существо для перемещения
            board: Игровая доска
            logger: Логгер для записи действий
        """
        move_result = creature.make_move(board)
        
        # Если перемещение вернуло булево значение (старая версия)
        if isinstance(move_result, bool):
            return
            
        # Если перемещение вернуло список действий
        if isinstance(move_result, (list, tuple)):
            self._log_actions(creature, move_result, logger)
            
    def _log_actions(self, creature: Creature, actions: List[Tuple[str, str]], logger) -> None:
        """
        Логирование действий существа.
        
        Args:
            creature: Существо, совершившее действия
            actions: Список действий для логирования
            logger: Логгер для записи действий
        """
        for action in actions:
            if isinstance(action, tuple) and len(action) == 2:
                logger.log_action(creature, action[0], action[1])

    def __repr__(self) -> str:
        return "MoveAction()"
