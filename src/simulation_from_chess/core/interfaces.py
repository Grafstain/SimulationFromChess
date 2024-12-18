from abc import ABC, abstractmethod

from .coordinates import Coordinates


class IBoard(ABC):
    @abstractmethod
    def is_valid_coordinates(self, coordinates: Coordinates) -> bool:
        """
        Проверка валидности координат.

        Args:
            coordinates: Проверяемые координаты

        Returns:
            bool: True если координаты валидны, False в противном случае
        """
        pass

    # @abstractmethod
    # def get_entity(self, coordinates: Coordinates):
    #     pass
    #
    # @abstractmethod
    # def move_entity(self, from_coords: Coordinates, to_coords: Coordinates) -> bool:
    #     pass

class IMovable(ABC):
    @abstractmethod
    def get_speed(self) -> int:
        pass

    @abstractmethod
    def can_move_to(self, coordinates: Coordinates) -> bool:
        pass