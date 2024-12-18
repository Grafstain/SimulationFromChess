from collections import deque
from ..core.coordinates import Coordinates
from ..entities.entity import Entity
from typing import List, Tuple, Optional, Set
from ..core.game_state import EntityState
# from ..core.board import Board
from ..core.interfaces import IBoard, IMovable
from ..utils.distance_calculator import DistanceCalculator


class Creature(Entity):
    # Словарь для хранения счетчиков каждого типа существ
    _creature_counters = {}

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
        self.available_moves: Set[Coordinates] = set()
        self.target_type = None  # Будет установлен в подклассах
        self.food_value = None  # Будет установлен в подклассах
        self.planned_action = None  # Планируемое действие на следующий ход
        self._performed_action = None  # Добавляем пол для хранения выполненного действия
        
        # Получаем имя класса существа
        class_name = self.__class__.__name__
        
        # Инициализируем счетчик для данного типа существ, если его еще нет
        if class_name not in self._creature_counters:
            self._creature_counters[class_name] = 0
        
        # Увеличиваем счетчик и присваиваем номер существу
        self._creature_counters[class_name] += 1
        self._number = self._creature_counters[class_name]

    def __str__(self) -> str:
        """Строковое представление существа с номером."""
        return f"{self.__class__.__name__}{self._number}"

    @classmethod
    def reset_counters(cls):
        """Сброс всех счетчиков существ."""
        cls._creature_counters.clear()

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
        self.available_moves = board.path_finder.get_available_moves(
            self.coordinates, 
            self.speed
        )

    def make_move(self, board) -> List[Tuple[str, str]]:
        """
        Базовая логика перемещения существа.
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
            self.planned_action = ("Отдыхает", f"здоровье {self.hp}/{self.max_hp}")
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Ищем цель
        target = self.find_target(board)
        if not target:
            self.planned_action = ("Ищет цель", "но не находит")
            board.update_entity_state(self)
            return [self.planned_action]
        
        # Если цель рядом, планируем взаимодействие
        if self._can_interact_with_target(target):
            self.planned_action = self._get_planned_interaction(target)
            board.update_entity_state(self)
            
            success, actions = self.interact_with_target(board, target)
            if success:
                self._performed_action = actions[0] if actions else None
                return actions
            return [("Неудачное взаимодействие", "цель избежала взаимодействия")]
        
        # Если не можем взаимодействовать, планируем движение к цели
        best_move = self._find_best_move(target.coordinates)
        if best_move:
            self.planned_action = ("Планирует передвижение", f"к {target.__class__.__name__}({target.coordinates.x}, {target.coordinates.y})")
            board.update_entity_state(self)
            
            if board.move_entity(self.coordinates, best_move):
                self._performed_action = ("Переместился", f"на ({best_move.x}, {best_move.y})")
                return [self._performed_action]
        
        self.planned_action = ("Не может двигаться", "путь заблокирован")
        board.update_entity_state(self)
        return [self.planned_action]

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
        """
        Поиск ближайшей цели определенного типа.
        
        Args:
            board: Игровая доска
        
        Returns:
            Optional[Entity]: Найденная цель или None
        """
        # Используем None вместо self.speed * 2 для поиска по всему полю
        return board.path_finder.find_nearest_target(
            self.coordinates,
            self.target_type,
            None  # Убираем ограничение видимости
        )

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
        return DistanceCalculator.is_adjacent(self.coordinates, target.coordinates)