from collections import deque
from ..core import Coordinates
from ..entities import Entity


class Creature(Entity):
    def __init__(self, coordinates: Coordinates, speed: int, hp: int):
        super().__init__(coordinates)
        self.speed = speed  # Скорость передвижения
        self.hp = hp  # Очки здоровья
        self.available_moves = []

    def update_available_moves(self, board):
        """Обновляет список доступных ходов с учетом препятствий."""
        available = []
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed, self.speed + 1):
                if abs(dx) + abs(dy) <= self.speed:  # Манхэттенское расстояние
                    new_x = self.coordinates.x + dx
                    new_y = self.coordinates.y + dy
                    new_coord = Coordinates(new_x, new_y)
                    
                    if (1 <= new_x <= board.width and 
                        1 <= new_y <= board.height and 
                        board.is_square_empty(new_coord) and
                        self.is_path_clear(board, new_coord)):
                        available.append(new_coord)
                        
        self.available_moves = available

    def is_path_clear(self, board, target):
        """Проверяет, свободен ли путь до целевой клетки."""
        dx = target.x - self.coordinates.x
        dy = target.y - self.coordinates.y
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return True
            
        step_x = dx / steps
        step_y = dy / steps
        
        current_x = self.coordinates.x
        current_y = self.coordinates.y
        
        for _ in range(steps):
            current_x += step_x
            current_y += step_y
            check_coord = Coordinates(round(current_x), round(current_y))
            if not board.is_square_empty(check_coord):
                return False
                
        return True

    def find_closest_food(self, board, food_type):
        """Находит ближайшую пищу с использованием манхэттенского расстояния."""
        closest_food = None
        min_distance = float('inf')
        
        # Проверяем все сущности на доске вместо только доступных ходов
        for coordinates, entity in board.entities.items():
            if isinstance(entity, food_type):
                distance = abs(coordinates.x - self.coordinates.x) + abs(coordinates.y - self.coordinates.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_food = coordinates
                
        return closest_food

    def make_move(self, board):
        """Базовая логика перемещения существа."""
        self.update_available_moves(board)
        target = self.find_closest_food(board, self.target_type)
        
        if target:
            best_move = self.find_best_move_towards(board, target)
            if best_move:
                self.perform_move(board, best_move)

    def find_best_move_towards(self, board, target):
        """Находит оптимальный ход в направлении цели."""
        best_move = None
        min_distance = float('inf')
        
        for move in self.available_moves:
            distance = abs(move.x - target.x) + abs(move.y - target.y)
            if distance < min_distance:
                min_distance = distance
                best_move = move
                
        return best_move
        
    def perform_move(self, board, new_coordinates):
        """Выполняет перемещение с обновлением состояния доски."""
        old_coordinates = self.coordinates
        board.remove_piece(old_coordinates)
        board.set_piece(new_coordinates, self)
        self.coordinates = new_coordinates
        print(f"{self} moved from {old_coordinates} to {new_coordinates}")