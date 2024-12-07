from abc import ABC
from ..core.Coordinates import Coordinates


class Entity(ABC):
    def __init__(self, coordinates: Coordinates):
        self.coordinates = coordinates
