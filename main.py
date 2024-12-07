from src.simulation_from_chess.core import *
from src.simulation_from_chess.actions import SpawnGrassAction
from src.simulation_from_chess.actions.HealthCheckAction import HealthCheckAction
from src.simulation_from_chess.actions.InitAction import InitAction
from src.simulation_from_chess.actions.MoveAction import MoveAction
import time

# Создание симуляции
simulation = Simulation()

# Добавление действий
simulation.init_actions.extend([
    InitAction()  # Начальная расстановка
])

simulation.turn_actions.extend([
    SpawnGrassAction(min_grass=3, spawn_chance=0.3),  # Спавн травы
    MoveAction(),  # Передвижение существ
    HealthCheckAction()  # Проверка здоровья
])

try:
    # Запуск симуляции
    simulation.start()
except KeyboardInterrupt:
    # Обработка Ctrl+C для корректного завершения
    simulation.pause_simulation()
    print("\nСимуляция завершена пользователем")
