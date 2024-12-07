"""Конфигурация параметров симуляции."""

# Параметры существ
CREATURE_CONFIG = {
    'herbivore': {
        'speed': 2,          # Скорость передвижения травоядных
        'initial_hp': 10,    # Начальное здоровье
        'food_value': 5,     # Сколько HP восстанавливает одна единица травы
    },
    'predator': {
        'speed': 3,          # Скорость передвижения хищников
        'initial_hp': 15,    # Начальное здоровье
        'attack_damage': 4,  # Урон от атаки
        'food_value': 8,     # Сколько HP восстанавливает одна жертва
    }
}

# Параметры симуляции
SIMULATION_CONFIG = {
    'hunger_damage': 1,      # Урон от голода за ход
    'min_grass': 4,         # Минимальное количество травы на поле
    'grass_spawn_chance': 0.3,  # Шанс появления новой травы
    'initial_herbivores': 3,    # Начальное кол��чество травоядных
    'initial_predators': 2,     # Начальное количество хищников
    'initial_grass': 6,         # Начальное количество травы
    'board_size': 8,           # Размер поля (8x8)
    'turn_delay': 1.0,         # Задержка между ходами в секундах
} 