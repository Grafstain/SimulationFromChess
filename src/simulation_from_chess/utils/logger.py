from typing import Dict
from ..entities.creature import Creature
from tabulate import tabulate

class Logger:
    def __init__(self):
        self.actions_log = {}  # Словарь для хранения действий существ

    def log_action(self, creature, action_type, details=""):
        """Сохранение действия существа."""
        if creature in self.actions_log:
            self.actions_log[creature] += f"; {action_type} {details}"
        else:
            self.actions_log[creature] = f"{action_type} {details}"

    def log_creatures_state(self, entities: Dict):
        """Вывод состояния существ в табличном формате."""
        creatures_data = []
        
        for entity in entities.values():
            if isinstance(entity, Creature):
                action = self.actions_log.get(entity, "")
                creatures_data.append([
                    str(entity),
                    f"({entity.coordinates.x}, {entity.coordinates.y})",
                    entity.hp,
                    action
                ])
        
        if creatures_data:
            print("\nСостояние существ:")
            print(tabulate(
                creatures_data,
                headers=['Существо', 'Координаты', 'HP', 'Действие'],
                tablefmt='simple'
            ))