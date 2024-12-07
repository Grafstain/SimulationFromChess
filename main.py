from src.simulation_from_chess.core import *
from src.simulation_from_chess.actions import SpawnGrassAction
from src.simulation_from_chess.actions.HealthCheckAction import HealthCheckAction
from src.simulation_from_chess.actions.InitAction import InitAction
from src.simulation_from_chess.actions.MoveAction import MoveAction
from src.simulation_from_chess.actions.HungerAction import HungerAction
from src.simulation_from_chess.config import SIMULATION_CONFIG

# Создание симуляции с настроенным размером поля
simulation = Simulation(board_size=SIMULATION_CONFIG['board_size'])

# Добавление действий
simulation.init_actions.extend([
    InitAction(
        herbivores=SIMULATION_CONFIG['initial_herbivores'],
        predators=SIMULATION_CONFIG['initial_predators'],
        grass=SIMULATION_CONFIG['initial_grass']
    )
])

simulation.turn_actions.extend([
    SpawnGrassAction(
        min_grass=SIMULATION_CONFIG['min_grass'],
        spawn_chance=SIMULATION_CONFIG['grass_spawn_chance']
    ),
    MoveAction(),
    HungerAction(hunger_damage=SIMULATION_CONFIG['hunger_damage']),
    HealthCheckAction()
])

try:
    simulation.start()
except KeyboardInterrupt:
    simulation.stop_simulation()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    simulation.stop_simulation()
finally:
    print("Программа завершена.")
