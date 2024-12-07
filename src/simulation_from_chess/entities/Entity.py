from abc import ABC
from ..core import Coordinates


class Entity(ABC):
    def __init__(self, coordinates: Coordinates):
        self.coordinates = coordinates
