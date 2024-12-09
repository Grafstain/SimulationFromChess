from src.simulation_from_chess import (
    Simulation,
    SpawnGrassAction,
    MoveAction,
    HealthCheckAction,
    HungerAction,
    InitAction,
    SIMULATION_CONFIG
)

# Создание симуляции с настроенным размером поля
simulation = Simulation(board_size=SIMULATION_CONFIG['board_size'])

# Добавление действий
simulation.init_actions.extend([
    InitAction(
        herbivores=SIMULATION_CONFIG['initial_herbivores'],
        predators=SIMULATION_CONFIG['initial_predators'],
        grass=SIMULATION_CONFIG['initial_grass'],
        stones=SIMULATION_CONFIG['initial_stones']
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
# except Exception as e:
#     print(f"Произшла ошибка: {e.}")
#     simulation.stop_simulation()
finally:
    print("Программа завершена.")
