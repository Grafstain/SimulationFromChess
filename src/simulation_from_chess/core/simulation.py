from ..actions.init_action import InitAction
from ..core.board import Board
from ..entities.creature import Creature
from ..renderers.board_console_renderer import BoardConsoleRenderer
from ..utils.logger import Logger
from ..config import SIMULATION_CONFIG
import time
import keyboard


class Simulation:
    def __init__(self, size: int = None):
        """Инициализация симуляции."""
        if size is None:
            size = SIMULATION_CONFIG['board_size']
        
        self.board = Board(size, size)
        self.renderer = BoardConsoleRenderer()
        self.logger = Logger()
        self.move_counter = 0
        self.is_running = False
        self.is_paused = False
        self.turn_actions = []

    def initialize(self, herbivores: int = 0, predators: int = 0, grass: int = 0, stones: int = 0) -> None:
        """
        Инициализация симуляции с заданным количеством сущностей.
        
        Args:
            herbivores: Количество травоядных
            predators: Количество хищников
            grass: Количество травы
            stones: Количество камней
        """
        # Очищаем доску перед инициализацией
        self.board.entities.clear()
        self.is_running = False
        self.move_counter = 0
        
        init_action = InitAction(
            herbivores=herbivores,
            predators=predators,
            grass=grass,
            stones=stones
        )
        init_action.execute(self.board, self.logger)
        
        # Проверяем наличие существ
        creatures_exist = any(
            isinstance(entity, Creature)
            for entity in self.board.entities.values()
        )
        self.is_running = creatures_exist

    def place_entity(self, entity, coordinates):
        """
        Размещение сущности на доске и обновление состояния симуляции.
        
        Args:
            entity: Размещаемая сущность
            coordinates: Координаты для размещения
        """
        self.board.place_entity(coordinates, entity)
        if isinstance(entity, Creature):
            self.is_running = True

    def next_turn(self) -> bool:
        """
        Выполнение следующег�� хода симуляции.
        
        Returns:
            bool: True если симуляция должна продолжаться, False если нужно остановиться
        """
        if not self.is_running:
            return False

        # Проверяем наличие живых существ на доске
        living_creatures_exist = any(
            isinstance(entity, Creature) and entity.hp > 0
            for entity in self.board.entities.values()
        )
        
        if not living_creatures_exist:
            self.is_running = False
            print("Симуляция завершена: на поле не осталось живых существ")
            return False

        # Выполняем все действия хода
        for action in self.turn_actions:
            action.execute(self.board, self.logger)

        # Обновляем состояние
        self.move_counter += 1
        self.renderer.render(self.board)
        self.logger.print_logs()

        return True

    def run(self, steps: int = None) -> None:
        """Запуск симуляции."""
        print("\n=== Симуляция запущена ===")
        
        # Проверяем наличие существ перед запуском
        if not any(isinstance(entity, Creature) for entity in self.board.entities.values()):
            print("Симуляция не может быть запущена: нет существ на поле")
            return
        
        current_step = 0
        self.is_running = True  # Устанавливаем флаг только если есть существа
        
        while self.is_running:
            if steps is not None and current_step >= steps:
                print("\nДостигнуто максимальное количество ходов")
                break
            
            if keyboard.is_pressed('q'):
                self.stop_simulation()
                break
            
            if keyboard.is_pressed('space'):
                self.toggle_pause()
                time.sleep(0.3)
            
            if not self.is_paused:
                if not self.next_turn():
                    break
                
                if steps is not None:
                    current_step += 1
                
                time.sleep(SIMULATION_CONFIG['turn_delay'])

    def stop_simulation(self) -> None:
        """Остановка симуляции."""
        self.is_running = False
        print("\n=== Симуляция остановлена ===")

    def toggle_pause(self) -> None:
        """Переключение паузы симуляции."""
        self.is_paused = not self.is_paused
        status = "поставлена на паузу" if self.is_paused else "возобновлена"
        print(f"\n=== Симуляция {status} ===")
