"""
Конфигурация параметров симуляции.
Этот модуль содержит все настраиваемые параметры для существ и симуляции в целом.
"""

# Параметры существ
CREATURE_CONFIG = {
    'herbivore': {
        'speed': 1,          # Скорость передвижения травоядных (клеток за ход)
        'initial_hp': 70,    # Начальное здоровье
        'food_value': 20,     # Восстановление HP при поедании травы
    },
    'predator': {
        'speed': 2,          # Скорость передвижения хищников (клеток за ход)
        'initial_hp': 100,   # Начальное здоровье
        'attack_damage': 30, # Урон от атаки
        'food_value': 30,    # Восстановление HP при поедании жертвы
        'escape_chance': 0.3,  # 30% шанс для травоядного убежать
    }
}

# Параметры симуляции
SIMULATION_CONFIG = {
    'board_size': 10,
    'initial_herbivores': 3,
    'initial_predators': 2,
    'initial_grass': 4,
    'initial_stones': 3,
    'min_grass': 4,
    'grass_spawn_chance': 0.3,
    'hunger_damage': 5,
    'max_turns': 100,
    'turn_delay': 1.0
}