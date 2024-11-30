from Board import Board
from BoardConsoleRenderer import BoardConsoleRenderer

# Создание доски
board = Board()
renderer = BoardConsoleRenderer()

# Установка существ на доске
board.setup_random_positions()
renderer.render(board)
