from typing import Dict, Any
from ..entities.entity import Entity


class BoardState:
    def __init__(self):
        self.current_turn = 0
        self.entity_states: Dict[int, Dict[str, Dict[str, Any]]] = {}
        
    def save_entity_state(self, turn: int, entity_id: str, state: Dict[str, Any]) -> None:
        """
        Сохранение состояния сущности.
        """
        if turn not in self.entity_states:
            self.entity_states[turn] = {}
        self.entity_states[turn][entity_id] = state
        
    def get_entity_state(self, turn: int, entity_id: str) -> Dict[str, Any]:
        """
        Получение состояния сущности.
        """
        return self.entity_states.get(turn, {}).get(entity_id, {}) 