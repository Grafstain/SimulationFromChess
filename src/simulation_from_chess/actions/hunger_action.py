from ..actions.action import Action
from ..entities.creature import Creature
from ..core.board import Board
from ..utils.logger import Logger


class HungerAction(Action):
    def __init__(self, hunger_damage: int):
        self.hunger_damage = hunger_damage
        self.dead_entities = {}  # Словарь для хранения мертвых существ и их координат

    def execute(self, board: Board, logger: Logger) -> None:
        """
        Применяет урон от голода ко всем существам.
        
        Args:
            board: Игровое поле
            logger: Логгер для записи действий
        """
        # Сначала удаляем существ, умерших на прошлом ходу
        for coordinates, entity in self.dead_entities.items():
            board.remove_entity(coordinates)
        self.dead_entities.clear()
        
        # Обрабатываем текущий ход
        for coordinates, entity in board.entities.items():
            if isinstance(entity, Creature):
                # Применяем урон от голода
                old_hp = entity.hp
                entity.take_damage(self.hunger_damage)
                
                # Если существо погибло, добавляем в список мертвых
                if entity.hp <= 0:
                    logger.log_action(entity, "Погиб", f"от голода на координатах ({coordinates.x}, {coordinates.y})")
                    self.dead_entities[coordinates] = entity