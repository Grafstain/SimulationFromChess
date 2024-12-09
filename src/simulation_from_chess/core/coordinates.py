class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Сравнение двух объектов Coordinates."""
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        """Хеширование для использования в словарях и множествах."""
        return hash((self.x, self.y))

    def __repr__(self):
        """Строковое представление координат для удобства отладки."""
        return f"Coordinates({self.x}, {self.y})"
