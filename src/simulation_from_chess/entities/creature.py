from collections import deque
from ..core.coordinates import Coordinates
from ..entities.entity import Entity
from typing import List, Tuple


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
        self.target_type = None  # Будет установлен в подклассах

    def update_available_moves(self, board):
        """Обновление списка доступных ходов с учетом скорости существа."""
        self.available_moves = []
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed + abs(dx), self.speed - abs(dx) + 1):
                new_x = self.coordinates.x + dx
                new_y = self.coordinates.y + dy
                new_coords = Coordinates(new_x, new_y)
                
                # Проверяем, что ход в пределах доски и позиция с��ободна
                if (board.is_within_bounds(new_coords) and 
                    board.is_position_vacant(new_coords)):
                    self.available_moves.append(new_coords)

    def make_move(self, board) -> List[Tuple[str, str]]:
        """
        Базовая логика перемещения существа.
        
        Returns:
            List[Tuple[str, str]]: Список действий для логирования
        """
        self.update_available_moves(board)
        if not self.available_moves:
            return []
            
        target = self.find_target(board)
        if not target:
            return []
            
        # Находим оптимальный ход в направлении цели
        best_move = self._find_best_move(target.coordinates)
        if best_move:
            if self._perform_move(board, best_move):
                # Проверяем, можем ли взаимодействовать с целью после перемещения
                if (abs(self.coordinates.x - target.coordinates.x) + 
                    abs(self.coordinates.y - target.coordinates.y)) <= 1:
                    success, actions = self.interact_with_target(board, target)
                    if success:
                        return actions
                return [("Переместился", f"на координаты ({best_move.x}, {best_move.y})")]
        return []

    def _find_best_move(self, target_coords):
        """Поиск оптимального хода в направлении цели."""
        if not self.available_moves:
            return None
            
        # Сортируем доступные ходы по расстоянию до цели
        sorted_moves = sorted(
            self.available_moves,
            key=lambda move: (
                abs(move.x - target_coords.x) + 
                abs(move.y - target_coords.y)
            )
        )
        
        # Фильтруем ходы, которые не превышают скорость существа
        valid_moves = [
            move for move in sorted_moves
            if (abs(move.x - self.coordinates.x) + 
                abs(move.y - self.coordinates.y)) <= self.speed
        ]
        
        return valid_moves[0] if valid_moves else None

    def _perform_move(self, board, new_coords):
        """Выполнение перемещения на новые координаты."""
        if board.move_entity(self.coordinates, new_coords):
            self.coordinates = new_coords
            return True
        return False

    def take_damage(self, damage):
        """Получение урона существом."""
        self.hp -= damage

    def interact_with_target(self, board, target):
        """Абстрактный метод взаимодействия с целью."""
        raise NotImplementedError("Subclasses should implement this method.")

    def find_target(self, board):
        """Поиск ближайшей цели определенного типа."""
        nearest_target = None
        min_distance = float('inf')
        
        for entity in board.entities.values():
            if isinstance(entity, self.target_type):
                distance = (abs(entity.coordinates.x - self.coordinates.x) + 
                          abs(entity.coordinates.y - self.coordinates.y))
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = entity
                    
        return nearest_target