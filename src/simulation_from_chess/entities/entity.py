from abc import ABC
from ..core.coordinates import Coordinates
from ..core.game_state import EntityState


class Entity(ABC):
    def __init__(self, coordinates: Coordinates):
        self.coordinates = coordinates
        self.entity_id = None  # Будет установлен при размещении на доске

    def get_state(self) -> EntityState:
        """Получение текущего состояния сущности."""
        return EntityState(coordinates=self.coordinates)
