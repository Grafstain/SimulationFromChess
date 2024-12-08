from collections import deque
from ..core.Coordinates import Coordinates
from ..entities.Entity import Entity


class Creature(Entity):
    def __init__(self, coordinates: Coordinates, speed: int, hp: int):
        """
        Инициализация базового класса существа.
        
        Args:
            coordinates (Coordinates): Координаты существа
            speed (int): Скорость передвижения
            hp (int): Начальное количество здоровья
        """
        super().__init__(coordinates)
        self.speed = speed
        self.hp = hp
        self.available_moves = []

    def update_available_moves(self, board):
        """Обновляет список доступных ходов с учетом всех ограничений."""
        self.available_moves = []
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed, self.speed + 1):
                if dx == 0 and dy == 0:  # Пропускаем текущую позицию
                    continue
                
                new_x = self.coordinates.x + dx
                new_y = self.coordinates.y + dy
                new_coord = Coordinates(new_x, new_y)
                
                if self.is_valid_move(board, new_coord):
                    self.available_moves.append(new_coord)

    def is_valid_move(self, board, coordinates):
        """Проверяет, является ли ход допустимым."""
        if not board.is_valid_coordinates(coordinates):
            return False
        
        if not board.is_square_empty(coordinates):
            return False
        
        if not self.has_clear_path(board, coordinates):
            return False
        
        return True

    def has_clear_path(self, board, target_coord):
        """Проверяет, свободен ли путь к целевой клетке."""
        dx = target_coord.x - self.coordinates.x
        dy = target_coord.y - self.coordinates.y
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return True
        
        step_x = dx / steps
        step_y = dy / steps
        
        current_x = self.coordinates.x
        current_y = self.coordinates.y
        
        # Проверяем каждую клетку на пути
        for _ in range(steps):
            current_x += step_x
            current_y += step_y
            check_coord = Coordinates(round(current_x), round(current_y))
            
            # Пропускаем проверку для конечной точки, так как она уже проверена
            if check_coord == target_coord:
                continue
            
            if not board.is_square_empty(check_coord):
                return False
            
        return True

    def find_closest_food(self, board, food_type):
        """Находит ближайшую пищу с использованием манхэттенского расстояния."""
        closest_food = None
        min_distance = float('inf')
        
        for coordinates, entity in board.entities.items():
            if (isinstance(entity, food_type) and 
                board.is_valid_coordinates(coordinates)):
                distance = abs(coordinates.x - self.coordinates.x) + abs(coordinates.y - self.coordinates.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_food = coordinates
                
        return closest_food

    def make_move(self, board):
        """Базовая логика перемещения существа."""
        self.update_available_moves(board)  # Обновляем доступные ходы
        
        if not self.available_moves:  # Если нет доступных ходов
            return []
        
        target = self.find_closest_food(board, self.target_type)
        if not target:  # Если нет цели
            return []
        
        # Если цель рядом
        distance = abs(target.x - self.coordinates.x) + abs(target.y - self.coordinates.y)
        if distance <= 1:
            target_entity = board.get_piece(target)
            if target_entity:
                success, actions = self.interact_with_target(board, target_entity)
                return actions if success else []
            
        # Ищем лучший ход среди доступных
        best_move = self.find_best_move_towards(board, target)
        if best_move:
            old_coords = self.coordinates
            self.perform_move(board, best_move)
            return [("Перемещение", f"из ({old_coords.x}, {old_coords.y}) в ({self.coordinates.x}, {self.coordinates.y})")]
        
        return []

    def find_best_move_towards(self, board, target):
        """Находит оптимальный ход в направлении цели."""
        best_move = None
        min_distance = float('inf')
        
        for move in self.available_moves:
            # Проверяем, что координаты в пределах поля
            if 0 <= move.x < board.width and 0 <= move.y < board.height:
                distance = abs(move.x - target.x) + abs(move.y - target.y)
                if distance < min_distance:
                    min_distance = distance
                    best_move = move
            
        return best_move
        
    def perform_move(self, board, new_coordinates):
        """Выполняет перемещение существа."""
        if new_coordinates in self.available_moves:  # Проверяем, что ход доступен
            old_coordinates = self.coordinates
            board.remove_piece(old_coordinates)
            board.set_piece(new_coordinates, self)
            self.coordinates = new_coordinates

    def take_damage(self, damage):
        """Получение урона существом."""
        self.hp -= damage

    def interact_with_target(self, board, target):
        """Абстрактный метод взаимодействия с целью."""
        raise NotImplementedError("Subclasses should implement this method.")