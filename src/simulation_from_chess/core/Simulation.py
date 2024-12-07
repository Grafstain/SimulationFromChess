from .Board import Board
from ..renderers import BoardConsoleRenderer


class Simulation:
    def __init__(self):
        self.board = Board()  # Инициализация карты
        self.move_counter = 0  # Счетчик ходов
        self.renderer = BoardConsoleRenderer()  # Рендерер поля
        self.init_actions = []  # Действия перед стартом симуляции
        self.turn_actions = []  # Действия на каждом ходе
        # self.board.setup_random_positions()


    def next_turn(self):
        """Просимулировать и отрендерить один ход."""
        print(f"Turn {self.move_counter + 1}:")

        # Выполнение действий на текущем ходе
        for action in self.turn_actions:
            action.execute(self.board)

        # Рендеринг состояния доски
        self.renderer.render(self.board)

        # Увеличение счетчика ходов
        self.move_counter += 1

    def start_simulation(self):
        """Запустить бесконечный цикл симуляции и рендеринга."""
        print("Starting simulation...")

        # Выполнение действий перед стартом симуляции
        for action in self.init_actions:
            action.execute(self.board)
        self.next_turn()
##TODO: поправить рендер клеток при старте
        # while True:
        #     self.next_turn()
            # Здесь можно добавить задержку или условие для выхода из цикла

    def pause_simulation(self):
        """Приостановить бесконечный цикл симуляции и рендеринга."""
        print("Simulation paused.")
        # Логика для приостановки симуляции (например, использование флага)