class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __lt__(self, other) -> bool:
        """Определение операции 'меньше' для сравнения координат."""
        if not isinstance(other, Coordinates):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
