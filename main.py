from InitAction import InitAction
from MoveAction import MoveAction
from Simulation import Simulation

# Создание симуляции
simulation = Simulation()

# Добавление действий
simulation.init_actions.append(InitAction())
simulation.turn_actions.append(MoveAction())

# Запуск симуляции
simulation.start_simulation()
simulation.next_turn()
# simulation.next_turn()
