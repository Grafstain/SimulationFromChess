from .board import Board
from ..actions.init_action import InitAction
from ..renderers.board_console_renderer import BoardConsoleRenderer
from ..config import SIMULATION_CONFIG
from ..utils.logger import Logger
from ..entities.creature import Creature
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
        """Просимулировать и отрендерить один ход."""
        print(f"\nХод {self.move_counter + 1}")
        self.logger.actions_log.clear()

        # Если симуляция на паузе, не выполняем ход
        if self.is_paused:
            return False

        # Проверяем наличие существ
        creatures = self.board.get_entities_by_type(Creature)
        if not creatures:
            print("\nСимуляция завершена: все существа погибли")
            self.stop_simulation()
            return False

        for action in self.turn_actions:
            action.execute(self.board, self.logger)

        self.renderer.render(self.board)
        self.logger.log_creatures_state(self.board.entities)
        self.move_counter += 1
        return True

    def start(self, run_loop=True):
        """
        Запустить симуляцию.
        
        Args:
            run_loop: Если True, запускает бесконечный цикл симуляции (по умолчанию)
                     Если False, только инициализирует симуляцию (для тестирования)
        """
        print("Начало симуляции")
        print("Управление: ПРОБЕЛ - пауза/продолжить, q - остановить симуляцию")

        for action in self.init_actions:
            action.execute(self.board, self.logger)

        self.is_running = True

        if run_loop:
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
        """Запустить симуляцию на заданное количество шагов."""
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
                if not self.next_turn():  # Проверяем результат выполнения хода
                    break  # Прерываем цикл, если ход не выполнен
                steps_completed += 1
                time.sleep(self.turn_delay)

    def initialize(self, herbivores: int = 0, predators: int = 0, grass: int = 0) -> None:
        """
        Инициализация начального состояния симуляции.
        
        Args:
            herbivores: Количество травоядных
            predators: Количество хищников
            grass: Количество травы
        """
        init_action = InitAction(
            herbivores=herbivores,
            predators=predators,
            grass=grass
        )
        init_action.execute(self.board, self.logger)
