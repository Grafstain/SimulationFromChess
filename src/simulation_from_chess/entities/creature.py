from collections import deque
from ..core.coordinates import Coordinates
from ..entities.entity import Entity
from typing import List, Tuple, Optional
from ..core.game_state import EntityState


class Creature(Entity):
    def __init__(self, coordinates: Coordinates, hp: int, speed: int):
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
        self.max_hp = hp
        self.available_moves = []
        self.target_type = None  # Будет установлен в подклассах
        self.food_value = None  # Будет установлен в подклассах
        self.planned_action = None  # Планируемое действие на следующий ход
        self._performed_action = None  # Добавляем пол для хранения выполненного действия

    def get_state(self) -> EntityState:
        """Получение текущего состояния существа."""
        return EntityState(
            coordinates=self.coordinates,
            hp=self.hp,
            planned_action=self.planned_action,
            performed_action=self._performed_action
        )

    def update_available_moves(self, board):
        """Обновление списка доступных ходов с учетом скорости существа."""
        self.available_moves = []
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed + abs(dx), self.speed - abs(dx) + 1):
                new_x = self.coordinates.x + dx
                new_y = self.coordinates.y + dy
                new_coords = Coordinates(new_x, new_y)
                
                # Проверяем, что ход в пределах доски и позиция свободна
                if (board.is_valid_coordinates(new_coords) and 
                    board.is_position_vacant(new_coords)):
                    self.available_moves.append(new_coords)

    def make_move(self, board) -> List[Tuple[str, str]]:
        """
        Базовая логика перемещения существа.
        
        Returns:
            List[Tuple[str, str]]: Список действий для логирования
        """
        self._performed_action = None
        self.update_available_moves(board)
        
        # Если нет доступных ходов
        if not self.available_moves:
            self.planned_action = ("Ожидает", "нет доступных ходов")
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Если существу не нужна еда
        if not self.needs_food():
            self.planned_action = ("Отдыхает", "")
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Ищем цель
        target = self.find_target(board)
        if not target:
            self.planned_action = ("Цель", "не найдена")
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Проверяем, было ли уже запланировано действие
        if not hasattr(self, '_has_planned') or not self._has_planned:
            # Находим лучший ход к цели для планирования
            best_move = self._find_best_move(target.coordinates)
            if not best_move:
                self.planned_action = ("Не может достичь", f"цель на ({target.coordinates.x}, {target.coordinates.y})")
            else:
                # Если цель рядом, планируем съесть
                if self._can_interact_with_target(target):
                    self.planned_action = self._get_planned_interaction(target)
                else:
                    self.planned_action = ("Планирует движение", f"к {str(target)} на ({target.coordinates.x}, {target.coordinates.y})")
            
            self._has_planned = True
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Сбрасываем флаг планирования для следующего хода
        self._has_planned = False
        
        # Проверяем, существует ли всё ещё цель
        target = self.find_target(board)
        if not target:
            self._performed_action = ("Цель", "исчезла")
            board.update_entity_state(self)
            return [self._performed_action]
        
        # Если цель рядом, пытаемся взаимодействовать
        if self._can_interact_with_target(target):
            success, actions = self.interact_with_target(board, target)
            if success:
                self._performed_action = actions[-1] if actions else None
                board.update_entity_state(self)
                return actions
        
        # Если не можем взаимодействовать, двигаемся к цели
        best_move = self._find_best_move(target.coordinates)
        if best_move and board.move_entity(self.coordinates, best_move):
            self._performed_action = ("Переместился", f"на координаты ({best_move.x}, {best_move.y})")
            board.update_entity_state(self)
            return [self._performed_action]
        
        return []

    def _find_best_move(self, target_coords: Coordinates) -> Optional[Coordinates]:
        """
        Находит лучший ход в направлении цели.
        
        Args:
            target_coords: Координаты цели
        
        Returns:
            Optional[Coordinates]: Координаты лучшего хода или None
        """
        if not self.available_moves:
            return None
        
        # Сортируем доступные ходы по расстоянию до цели
        moves_with_distances = [
            (move, abs(move.x - target_coords.x) + abs(move.y - target_coords.y))
            for move in self.available_moves
        ]
        moves_with_distances.sort(key=lambda x: x[1])
        
        # Возвращаем ход с минимальным расстоянием до цели
        return moves_with_distances[0][0] if moves_with_distances else None

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

    def heal(self, amount: int):
        """
        Восстановление здоровья существа.
        
        Args:
            amount (int): Количество восстанавливаемого здоровья
        """
        self.hp += amount

    def needs_food(self) -> bool:
        """
        Проверяет, нужно ли существу икать пищу.
        
        Returns:
            bool: True если существу нужна пища, False в противном случае
        """
        if self.food_value is None:
            return True
        # Существо ищет пищу, если его текущее HP меньше чем (максимальное HP - питательность пищи)
        return self.hp < (self.max_hp - self.food_value)

    def _get_planned_interaction(self, target) -> Tuple[str, str]:
        """
        Получение описания планируемого взаимодействия с целью.
        Должен быть переопределен в подклассах.
        """
        return ("Планирует взаимодействие", f"с целью на ({target.coordinates.x}, {target.coordinates.y})")

    def _can_interact_with_target(self, target) -> bool:
        """Проверка возможности взаимодействия с целью."""
        return (abs(self.coordinates.x - target.coordinates.x) + 
                abs(self.coordinates.y - target.coordinates.y)) <= 1