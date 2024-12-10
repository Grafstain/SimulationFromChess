from typing import Dict
from ..entities.creature import Creature
from tabulate import tabulate

class Logger:
    def __init__(self):
        self.actions_log = {}  # Словарь для хранения действий существ
        self.dead_entities = {}  # Словарь для хранения мертвых существ

    def log_action(self, creature, action_type, details="", killer=None):
        """
        Сохранение действия существа.
        
        Args:
            creature: Существо, совершившее действие
            action_type: Тип действия
            details: Детали действия
            killer: Существо, убившее данное существо (если применимо)
        """
        action_text = action_type
        if details:  # Добавляем детали только если они не пустые
            action_text += f" {details}"
        
        # Записываем только одно действие для существа за ход
        self.actions_log[creature] = action_text
        
        # Если существо погибло, добавляем его в список мертвых
        if action_type == "Погиб":
            if killer:
                death_text = f"Был съеден существом {killer}"
            else:
                death_text = action_text
            self.dead_entities[creature] = (creature.coordinates, death_text)

    def log_creatures_state(self, entities: Dict):
        """Вывод состояния существ в табличном формате."""
        creatures_data = []
        
        # Добавляем живых существ
        for entity in entities.values():
            if isinstance(entity, Creature):
                action = self.actions_log.get(entity, "")
                creatures_data.append([
                    str(entity),
                    f"({entity.coordinates.x}, {entity.coordinates.y})",
                    entity.hp,
                    action
                ])
        
        # Добавляем мертвых существ
        for creature, (coords, action) in self.dead_entities.items():
            creatures_data.append([
                str(creature),
                f"({coords.x}, {coords.y})",
                0,
                action
            ])
        
        if creatures_data:
            print("\nСостояние существ:")
            print(tabulate(
                creatures_data,
                headers=['Существо', 'Координаты', 'HP', 'Действие'],
                tablefmt='simple'
            ))
        
        # Очищаем список мертвых существ после вывода
        self.dead_entities.clear()