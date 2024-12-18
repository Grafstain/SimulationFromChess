import random
from typing import TYPE_CHECKING, Tuple, List
from ..core.coordinates import Coordinates
from .creature import Creature
from .herbivore import Herbivore
from ..config import CREATURE_CONFIG
from ..utils.distance_calculator import DistanceCalculator

if TYPE_CHECKING:
    from ..core.board import Board

class Predator(Creature):
    def __init__(self, coordinates: Coordinates):
        config = CREATURE_CONFIG['predator']
        super().__init__(
            coordinates=coordinates,
            hp=config['initial_hp'],
            speed=config['speed']
        )
        self.attack_damage = config['attack_damage']
        self.hunt_success_chance = 1 - config['escape_chance']
        self.target_type = Herbivore
        self.food_value = config['food_value']
        self._force_hunt_result = None

    def __repr__(self):
        """Строковое представление хищника."""
        return "Хищник"

    def set_hunt_result(self, result: bool) -> None:
        """
        Установка результата охоты для тестирования.
        
        Args:
            result: True для успешной охоты, False для неудачной
        """
        self._force_hunt_result = result

    def try_attack_herbivore(self, target: Herbivore) -> bool:
        """
        Попытка атаковать травоядное с учетом шанса успешной охоты.
        
        Args:
            target: Травоядное-цель
            
        Returns:
            bool: True если атака успешна, False если охота не удалась
        """
        if self._force_hunt_result is not None:
            result = self._force_hunt_result
            self._force_hunt_result = None  # Сбрасываем после использования
            return result
        return random.random() <= self.hunt_success_chance

    def interact_with_target(self, board: 'Board', target: Creature) -> Tuple[bool, List[Tuple]]:
        """
        Взаимодействие хищника с целью (атака травоядного).
        
        Args:
            board: Игровое поле
            target: Цель атаки
            
        Returns:
            Tuple[bool, List[Tuple]]: (успешность атаки, список действий для логирования)
        """
        if not isinstance(target, Herbivore):
            return False, [("Ошибка", "Цель не является травоядным")]

        if not self.try_attack_herbivore(target):
            return False, [("Неудачная атака", "Травоядное успешно избежало атаки")]

        # Атака успешна, наносим урон
        target.take_damage(self.attack_damage)
        actions = [("Атака", f"нанесено {self.attack_damage} урона")]
        
        # Если цель погибла, восстанавливаем здоровье хищнику
        if target.hp <= 0:
            heal_amount = CREATURE_CONFIG['predator']['food_value']
            self.heal(heal_amount)
            board.remove_entity(target.coordinates)
            actions.extend([
                ("Успешная охота", f"здоровье восстановлено на {heal_amount}"),
                ("Погиб", "", target, self)  # Информация о смерти цели
            ])
        
        return True, actions

    def _get_planned_interaction(self, target) -> Tuple[str, str]:
        """Описание планируемой атаки хищника."""
        return ("Планирует атаковать", f"травоядное на ({target.coordinates.x}, {target.coordinates.y})")

    def find_target(self, board):
        """
        Поиск ближайшей жертвы (травоядного).
        
        Args:
            board: Игровая доска
        
        Returns:
            Optional[Entity]: Найденное травоядное или None
        """
        # Получаем все сущности типа Herbivore на поле
        herbivore_targets = [
            (entity, DistanceCalculator.manhattan_distance(self.coordinates, entity.coordinates))
            for entity in board.get_entities_by_type(Herbivore)
            if entity.hp > 0  # Проверяем, что травоядное живо
        ]
        
        # Сортируем по расстоянию и возвращаем ближайшее травоядное
        if herbivore_targets:
            herbivore_targets.sort(key=lambda x: x[1])
            return herbivore_targets[0][0]
        return None

    def needs_food(self) -> bool:
        """
        Проверяет, нужно ли хищнику искать пищу.
        
        Returns:
            bool: True если хищнику нужна пища, False в противном случае
        """
        # Хищник всегда ищет пищу, если его здоровье не максимальное
        return self.hp < self.max_hp

