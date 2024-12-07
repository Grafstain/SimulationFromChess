from src.simulation_from_chess.core import *
from src.simulation_from_chess.actions import SpawnGrassAction
from src.simulation_from_chess.actions.HealthCheckAction import HealthCheckAction
from src.simulation_from_chess.actions.InitAction import InitAction
from src.simulation_from_chess.actions.MoveAction import MoveAction

# Создание симуляции
simulation = Simulation()

# Добавление действий
simulation.init_actions.extend([
    InitAction()
])

simulation.turn_actions.extend([
    SpawnGrassAction(min_grass=3, spawn_chance=0.3),
    MoveAction(),
    HealthCheckAction()
])

try:
    # Запуск симуляции
    simulation.start()
except KeyboardInterrupt:
    simulation.stop_simulation()
except Exception as e:
    print(f"Произошла ошибка: {e}")
    simulation.stop_simulation()
finally:
    print("Программа завершена.")
