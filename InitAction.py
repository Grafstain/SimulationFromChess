from Action import Action


class InitAction(Action):
    def execute(self, board):
        print("Initializing board with entities...")
        board.setup_random_positions()  # Пример: установить 5 травоядных и 3 хищника

    def __repr__(self):
        return f"InitAction"