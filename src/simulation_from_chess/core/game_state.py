from dataclasses import dataclass
from typing import Dict, Optional, Any
from ..core.coordinates import Coordinates


@dataclass
class EntityState:
    """Состояние сущности на определенном ходу."""
    coordinates: Coordinates
    hp: Optional[int] = None
    planned_action: Optional[tuple] = None
    performed_action: Optional[tuple] = None


class GameState:
    """Класс для хранения состояния игры."""
    def __init__(self):
        self.current_turn = 0
        self.states: Dict[int, Dict[int, EntityState]] = {}  # turn -> {entity_id -> state}
        self._entity_id_counter = 0

    def get_new_entity_id(self) -> int:
        """Получение нового уникального ID для сущности."""
        self._entity_id_counter += 1
        return self._entity_id_counter

    def save_entity_state(self, turn: int, entity_id: int, state: EntityState) -> None:
        """Сохранение состояния сущности."""
        if turn not in self.states:
            self.states[turn] = {}
        self.states[turn][entity_id] = state

    def get_entity_state(self, turn: int, entity_id: int) -> Optional[EntityState]:
        """Получение состояния сущности на определенном ходу."""
        return self.states.get(turn, {}).get(entity_id)

    def get_previous_state(self, turn: int, entity_id: int) -> Optional[EntityState]:
        """Получение предыдущего состояния сущности."""
        return self.get_entity_state(turn - 1, entity_id)

    def clear_old_states(self, keep_turns: int = 2) -> None:
        """Очистка старых состояний, оставляя только последние n ходов."""
        turns_to_remove = sorted(self.states.keys())[:-keep_turns] if len(self.states) > keep_turns else []
        for turn in turns_to_remove:
            del self.states[turn] 