from .board import Board
from ..renderers.board_console_renderer import BoardConsoleRenderer
from ..config import SIMULATION_CONFIG
from ..utils.logger import Logger
import time
import keyboard


class Simulation:
    def __init__(self, board_size=8):
        """
        Инициализация симуляции.
        
        Args:
            board_size: Размер игрового поля
            
        Raises:
            ValueError: Если размер поля меньше или равен 0
        """
        if board_size <= 0:
            raise ValueError(f"Размер поля должен быть положительным числом, получено: {board_size}")
            
        self.logger = Logger()
        self.board = Board(board_size, board_size)
        self.move_counter = 0
        self.renderer = BoardConsoleRenderer()
        self.init_actions = []
        self.turn_actions = []
        self.is_running = False
        self.is_paused = False
        self.turn_delay = SIMULATION_CONFIG['turn_delay']

    def next_turn(self):
        """Просимулироват�� и отрендерить один ход."""
        print(f"\nХод {self.move_counter + 1}")
        self.logger.actions_log.clear()

        for action in self.turn_actions:
            action.execute(self.board, self.logger)

        self.renderer.render(self.board)
        self.logger.log_creatures_state(self.board.entities)
        self.move_counter += 1

    def start(self):
        """Запустить бесконечный цикл симуляции и рендеринга."""
        print("Начало симуляции")
        print("Управление: ПРОБЕЛ - пауза/продолжить, q - остановить симуляцию")

        for action in self.init_actions:
            action.execute(self.board, self.logger)

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
                time.sleep(self.turn_delay)

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

    def run(self, steps: int):
        """
        Запустить симуляцию на заданное количество шагов.
        
        Args:
            steps: Количество шагов симуляции
        """
        if steps <= 0:
            return
        
        print(f"Запуск симуляции на {steps} шагов")
        print("Управление: ПРОБЕЛ - пауза/продолжить, q - остановить симуляцию")

        # Выполняем инициализационные действия
        for action in self.init_actions:
            action.execute(self.board, self.logger)

        self.is_running = True
        steps_completed = 0
        
        while self.is_running and steps_completed < steps:
            if keyboard.is_pressed('space'):
                self.toggle_pause()
                time.sleep(0.1)
            elif keyboard.is_pressed('q'):
                self.stop_simulation()
                break

            if not self.is_paused:
                self.next_turn()
                steps_completed += 1
                time.sleep(self.turn_delay)
