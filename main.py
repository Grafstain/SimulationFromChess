from src.simulation_from_chess import (
    Simulation,
    SpawnGrassAction,
    MoveAction,
    HealthCheckAction,
    HungerAction,
    SIMULATION_CONFIG
)

def main():
    # Создание симуляции с настроенным размером поля
    simulation = Simulation(size=SIMULATION_CONFIG['board_size'])
    
    # Инициализируем симуляцию начальными существами
    simulation.initialize(
        herbivores=SIMULATION_CONFIG['initial_herbivores'],
        predators=SIMULATION_CONFIG['initial_predators'],
        grass=SIMULATION_CONFIG['initial_grass'],
        stones=SIMULATION_CONFIG['initial_stones']
    )
    
    # Добавляем действия для каждого хода
    simulation.turn_actions = [
        SpawnGrassAction(
            min_grass=SIMULATION_CONFIG['min_grass'],
            spawn_chance=SIMULATION_CONFIG['grass_spawn_chance']
        ),
        MoveAction(),
        HungerAction(hunger_damage=SIMULATION_CONFIG['hunger_damage']),
        HealthCheckAction()
    ]

    try:
        # Запускаем симуляцию
        simulation.run(steps=SIMULATION_CONFIG['max_turns'])
    except KeyboardInterrupt:
        simulation.stop_simulation()
    finally:
        print("Программа завершена.")

if __name__ == "__main__":
    main()
