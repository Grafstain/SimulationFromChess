from .Board import Board
from ..renderers.BoardConsoleRenderer import BoardConsoleRenderer
import time
import keyboard


class Simulation:
    def __init__(self, board_size=8):
        self.board = Board(board_size, board_size)
        self.move_counter = 0
        self.renderer = BoardConsoleRenderer()
        self.init_actions = []
        self.turn_actions = []
        self.is_running = False
        self.is_paused = False

    def next_turn(self):
        """Просимулировать и отрендерить один ход."""
        print(f"\nХод {self.move_counter + 1}:")

        for action in self.turn_actions:
            action.execute(self.board)

        self.renderer.render(self.board)
        self.renderer.display_common_creature_info(self.board)
        self.move_counter += 1

    def start(self):
        """Запустить бесконечный цикл симуляции и рендеринга."""
        print("Начало симуляции...")
        print("Управление:")
        print("  ПРОБЕЛ - пауза/продолжить")
        print("  q - остановить симуляцию")

        for action in self.init_actions:
            action.execute(self.board)

        self.is_running = True
        while self.is_running:
            if keyboard.is_pressed('space'):
                self.toggle_pause()
                time.sleep(0.1)
            elif keyboard.is_pressed('q'):
                self.stop_simulation()
                break

            if not self.is_paused:
                self.next_turn()
                time.sleep(1)

    def toggle_pause(self):
        """Переключить состояние паузы."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            print("\nСимуляция приостановлена. Нажмите ПРОБЕЛ для продолжения.")
        else:
            print("\nСимуляция возобновлена.")

    def stop_simulation(self):
        """Остановить симуляцию."""
        self.is_running = False
        print("\nСимуляция остановлена.")
