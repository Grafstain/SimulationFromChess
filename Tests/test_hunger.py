import unittest
from src.simulation_from_chess.core import Board
from src.simulation_from_chess.core.Coordinates import Coordinates
from src.simulation_from_chess.entities import Herbivore, Predator, Grass
from src.simulation_from_chess.actions.HungerAction import HungerAction
from src.simulation_from_chess.config import CREATURE_CONFIG


class TestHunger(unittest.TestCase):
    def setUp(self):
        """Создаем необходимые объекты перед каждым тестом."""
        self.board = Board(5, 5)
        self.hunger_action = HungerAction(hunger_damage=2)

    def test_basic_hunger_damage(self):
        """Тест базового урона от голода."""
        herbivore = Herbivore(Coordinates(1, 1))
        initial_hp = herbivore.hp
        self.board.set_piece(herbivore.coordinates, herbivore)

        self.hunger_action.execute(self.board)

        self.assertEqual(herbivore.hp, initial_hp - 2)
        self.assertEqual(initial_hp, CREATURE_CONFIG['herbivore']['initial_hp'])

    def test_multiple_creatures_hunger(self):
        """Тест урона от голода для нескольких существ."""
        herbivore = Herbivore(Coordinates(1, 1))
        predator = Predator(Coordinates(2, 2))
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(predator.coordinates, predator)

        self.hunger_action.execute(self.board)

        self.assertEqual(herbivore.hp, CREATURE_CONFIG['herbivore']['initial_hp'] - 2)
        self.assertEqual(predator.hp, CREATURE_CONFIG['predator']['initial_hp'] - 2)

    def test_eating_mechanics(self):
        """Тест механики питания."""
        herbivore = Herbivore(Coordinates(1, 1))
        grass = Grass(Coordinates(1, 2))
        
        # Наносим урон травоядному
        herbivore.take_damage(5)
        initial_hp = herbivore.hp
        
        self.board.set_piece(herbivore.coordinates, herbivore)
        self.board.set_piece(grass.coordinates, grass)
        
        herbivore.eat(grass)
        
        # Проверяем восстановление HP
        self.assertEqual(herbivore.hp, 
                        min(CREATURE_CONFIG['herbivore']['initial_hp'],
                            initial_hp + CREATURE_CONFIG['herbivore']['food_value']))

    def test_predator_eating_mechanics(self):
        """Тест механики питания хищника."""
        predator = Predator(Coordinates(1, 1))
        herbivore = Herbivore(Coordinates(1, 2))
        
        # Наносим урон хищнику
        predator.take_damage(5)
        initial_predator_hp = predator.hp
        
        self.board.set_piece(predator.coordinates, predator)
        self.board.set_piece(herbivore.coordinates, herbivore)
        
        predator.attack(herbivore)
        
        # Проверяем урон травоядному
        self.assertEqual(herbivore.hp, 
                        CREATURE_CONFIG['herbivore']['initial_hp'] - CREATURE_CONFIG['predator']['attack_damage']) 