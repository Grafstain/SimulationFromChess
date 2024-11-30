from abc import ABC
from Coordinates import Coordinates


class Entity(ABC):
    def __init__(self, coordinates: Coordinates):
        self.coordinates = coordinates
