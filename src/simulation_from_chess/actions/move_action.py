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
        # Создаем копию списка существ
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
        
        # Если результат пустой или не является списком/кортежем, пропускаем
        if not move_result or not isinstance(move_result, (list, tuple)):
            return
        
        # Если результат - список действий
        if isinstance(move_result[0], tuple):
            for action in move_result:
                if len(action) == 4:  # Действие с информацией о смерти
                    action_type, details, target, killer = action
                    logger.log_action(target, action_type, details, killer=killer)
                elif len(action) == 2:  # Обычное действие
                    logger.log_action(creature, action[0], action[1])
        # Если результат - одиночное действие в формате (success, action)
        elif len(move_result) == 2 and isinstance(move_result[1], str):
            success, action = move_result
            if success:
                logger.log_action(creature, "Действие", action)

    def __repr__(self) -> str:
        return "MoveAction()"
