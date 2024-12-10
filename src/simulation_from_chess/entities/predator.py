import random
from typing import TYPE_CHECKING, Tuple
from ..core.coordinates import Coordinates
from .creature import Creature
from .herbivore import Herbivore
from ..config import CREATURE_CONFIG

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

    def interact_with_target(self, board: 'Board', target: Creature) -> Tuple[bool, str]:
        """
        Взаимодействие хищника с целью (атака травоядного).
        
        Args:
            board: Игровое поле
            target: Цель атаки
            
        Returns:
            tuple[bool, str]: Успешность атаки и описание результата
        """
        if not isinstance(target, Herbivore):
            return False, "Цель не является травоядным"

        if not self.try_attack_herbivore(target):
            return False, "Травоядное успешно избежало атаки"

        # Атака успешна, наносим урон
        target.take_damage(self.attack_damage)
        
        # Если цель погибла, восстанавливаем здоровье хищнику
        if target.hp <= 0:
            self.heal(CREATURE_CONFIG['predator']['food_value'])
            # Возвращаем информацию о смерти в actions, чтобы MoveAction мог залогировать это
            board.remove_entity(target.coordinates)
            return True, [
                ("Успешная охота", f"здоровье восстановлено на {CREATURE_CONFIG['predator']['food_value']}"),
                ("Погиб", "", target, self)  # Добавляем информацию о цели и убийце
            ]
            
        return True, f"Успешная атака, нанесено {self.attack_damage} урона"

    def _get_planned_interaction(self, target) -> Tuple[str, str]:
        """Описание планируемой атаки хищника."""
        return ("Планирует атаковать", f"травоядное на ({target.coordinates.x}, {target.coordinates.y})")

