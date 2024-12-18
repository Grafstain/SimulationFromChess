from typing import Dict, Any, Optional
from tabulate import tabulate
from ..entities.creature import Creature

class Logger:
    def __init__(self):
        """Инициализация логгера."""
        self.creatures_state = {}  # Словарь для хранения состояния и действий существ
        self.system_logs = []      # Список для системных сообщений

    def clear_logs(self) -> None:
        """Очистка логов текущего хода."""
        self.system_logs.clear()
        # Очищаем только действия, сохраняя базовую информацию о существах
        for state in self.creatures_state.values():
            state['action'] = ''

    def log_action(self, entity, action_type: str, details: str, killer=None) -> None:
        """
        Логирование действия.
        
        Args:
            entity: Сущность, выполнившая действие
            action_type: Тип действия
            details: Детали действия
            killer: Сущность, вызвавшая смерть (опционально)
        """
        if entity is None:  # Системное сообщение
            if isinstance(details, str) and "Размещен" in details and "creature" not in details.lower():
                return  # Пропускаем логирование размещения не-существ
            self.system_logs.append(f"{action_type}: {details}")
            return

        entity_key = str(entity)
        if entity_key not in self.creatures_state:
            self.creatures_state[entity_key] = {
                'type': entity.__class__.__name__,
                'hp': getattr(entity, 'hp', 'N/A'),
                'coordinates': getattr(entity, 'coordinates', None),
                'action': ''
            }

        # Обновляем текущее состояние существа
        self.creatures_state[entity_key].update({
            'hp': getattr(entity, 'hp', 'N/A'),
            'coordinates': getattr(entity, 'coordinates', None)
        })

        if killer:
            action_text = f"{action_type} {details} (убит существом {killer})"
        else:
            if action_type == "Планирует":
                if "Планирует движение" in details:
                    action_text = details
                elif "Не может двигаться" in details:
                    action_text = "Не может двигаться: путь заблокирован"
                elif "Отдыхает" in details:
                    action_text = "Отдыхает"
                elif "Цель не найдена" in details:
                    action_text = "Цель не найдена"
                else:
                    action_text = f"{action_type}: {details}"
            else:
                action_text = f"{action_type} {details}"
        
        self.creatures_state[entity_key]['action'] = action_text

    def log_creatures_state(self, entities: dict) -> None:
        """
        Обновление состояния существ.
        
        Args:
            entities: Словарь сущностей на доске
        """
        # Создаем новый словарь состояний для всех существ на доске
        new_creatures_state = {}
        
        # Обновляем или добавляем новые состояния только для существ (Creature)
        for entity in entities.values():
            if isinstance(entity, Creature):
                entity_key = str(entity)
                # Сохраняем предыдущее действие, если оно было
                previous_action = self.creatures_state.get(entity_key, {}).get('action', '')
                
                new_creatures_state[entity_key] = {
                    'type': entity.__class__.__name__,
                    'hp': entity.hp,
                    'coordinates': entity.coordinates,
                    'action': previous_action
                }
        
        # Заменяем старый словарь состояний новым
        self.creatures_state = new_creatures_state

    def print_logs(self) -> None:
        """Вывод всех логов в табличном формате."""
        if self.system_logs:
            print("\nСистемные сообщения:")
            for log in self.system_logs:
                print(f"  {log}")
            self.system_logs.clear()

        if self.creatures_state:
            print("\nСостояние существ:")
            creatures_table = [
                [
                    name,
                    state['type'],
                    f"{state['hp']} HP",
                    f"({state['coordinates'].x}, {state['coordinates'].y})",
                    state['action']
                ]
                for name, state in self.creatures_state.items()
            ]
            print(tabulate(
                creatures_table,
                headers=['Существо', 'Тип', 'Здоровье', 'Координаты', 'Действие'],
                tablefmt='grid'
            ))