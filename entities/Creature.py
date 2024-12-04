from collections import deque

from Coordinates import Coordinates
from entities.Entity import Entity


class Creature(Entity):
    def __init__(self, coordinates: Coordinates, speed: int, hp: int):
        super().__init__(coordinates)
        self.speed = speed  # Скорость передвижения
        self.hp = hp  # Очки здоровья

    def make_move(self, board):
        """Перемещает существо на одну из доступных клеток."""
        available_moves = self.bfs_available_moves(board)

        if available_moves:
            # Перемещение на первую доступную клетку
            new_coordinates = available_moves[0]
            board.set_piece(new_coordinates, self)  # Устанавливаем существо на новую позицию
            board.remove_piece(self.coordinates)  # Убираем с предыдущей позиции
            self.coordinates = new_coordinates  # Обновляем координаты сущности
            # print(f"{self} moved to {new_coordinates}")

    def bfs_available_moves(self, board):
        """Ищет доступные клетки с помощью алгоритма BFS."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Вверх, вправо, вниз, влево
        queue = deque([self.coordinates])
        visited = set()
        available_moves = []

        while queue:
            current = queue.popleft()
            visited.add(current)

            for direction in directions:
                new_x = current.x + direction[0]
                new_y = current.y + direction[1]
                new_coord = Coordinates(new_x, new_y)

                if (1 <= new_x <= 8 and 1 <= new_y <= 8 and
                        board.is_square_empty(new_coord) and
                        new_coord not in visited):
                    available_moves.append(new_coord)
                    queue.append(new_coord)

        return available_moves