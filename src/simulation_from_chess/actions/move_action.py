from typing import List, Tuple, Union

from ..actions.action import Action
from ..entities import Entity
from ..entities.herbivore import Herbivore
from ..entities.predator import Predator
from ..entities.creature import Creature


class MoveAction(Action):
    def __init__(self):
        self.is_planning_phase = True  # Флаг для отслеживания фазы
        self.planned_entities = []  # Список существ с запланированными действиями

    def _format_target_description(self, target: Entity) -> str:
        """
        Форматирование описания цели для логов.
        
        Args:
            target: Целевая сущность
            
        Returns:
            str: Отформатированное описание цели
        """
        target_type = target.__class__.__name__
        if isinstance(target, Creature):
            # Для существ используем их полное имя (с номером)
            return f"{str(target)}"
        else:
            # Для остальных сущностей только координаты
            return f"{target_type} на ({target.coordinates.x}, {target.coordinates.y})"

    def execute(self, board, logger) -> None:
        """
        Перемещение всех существ на поле.
        
        Args:
            board: Игровая доска
            logger: Логгер для записи действий
        """
        # Обновляем состояние всех существ в начале действия
        logger.log_creatures_state(board.entities)
        
        entities = [
            entity for entity in board.entities.values()
            if isinstance(entity, (Herbivore, Predator))
        ]

        if self.is_planning_phase:
            # Фаза планирования
            self.planned_entities.clear()
            
            # Обновляем доступные ходы для всех существ
            for entity in entities:
                entity.update_available_moves(board)
            
            # Планируем действия и логируем их
            for entity in entities:
                target = entity.find_target(board)
                if target and entity.needs_food():
                    if entity._can_interact_with_target(target):
                        planned_action = entity._get_planned_interaction(target)
                    else:
                        best_move = entity._find_best_move(target.coordinates)
                        if best_move:
                            target_desc = self._format_target_description(target)
                            planned_action = (
                                "Планирует движение",
                                f"к {target_desc}"
                            )
                        else:
                            planned_action = (
                                "Не может двигаться",
                                "путь заблокирован"
                            )
                else:
                    if not entity.needs_food():
                        planned_action = ("Отдыхает", "сыт")
                    else:
                        planned_action = ("Ищет цель", "не найдена подходящая цель")
                
                entity.planned_action = planned_action
                board.update_entity_state(entity)
                logger.log_action(entity, planned_action[0], planned_action[1])
                self.planned_entities.append(entity)
        else:
            # Фаза выполнения
            for entity in self.planned_entities:
                if entity in entities:  # Проверяем, что существо всё ещё живо
                    old_coords = entity.coordinates  # Запоминаем старые координаты
                    move_result = entity.make_move(board)
                    
                    if not move_result or not isinstance(move_result, (list, tuple)):
                        continue
                    
                    # Логируем результаты действий
                    if isinstance(move_result[0], tuple):
                        for action in move_result:
                            if len(action) == 4:  # Действие с информацией о смерти
                                action_type, details, target, killer = action
                                logger.log_action(target, action_type, details, killer=killer)
                            elif len(action) == 2:  # Обычное действие
                                if action[0] == "Переместился":
                                    logger.log_action(
                                        entity,
                                        action[0],
                                        f"с ({old_coords.x}, {old_coords.y}) на {action[1]}"
                                    )
                                else:
                                    logger.log_action(entity, action[0], action[1])
        
        # Переключаем фазу
        self.is_planning_phase = not self.is_planning_phase
        
        # После выполнения всех действий обновляем состояние
        logger.log_creatures_state(board.entities)

    def __repr__(self) -> str:
        return "MoveAction()"
