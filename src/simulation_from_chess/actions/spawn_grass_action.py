from random import randint
from ..core.coordinates import Coordinates
from ..entities.grass import Grass
from .action import Action

class SpawnGrassAction(Action):
    def __init__(self, min_grass=3, spawn_chance=0.3):
        self.min_grass = min_grass
        self.spawn_chance = spawn_chance

    def execute(self, board, logger):
        """Добавляет траву на поле, если её слишком мало."""
        grass_count = sum(1 for entity in board.entities.values() 
                         if isinstance(entity, Grass))
        
        if grass_count < self.min_grass and randint(1, 100) / 100 <= self.spawn_chance:
            empty_coords = [
                Coordinates(x, y)
                for x in range(0, board.width)
                for y in range(0, board.height)
                if board.is_square_empty(Coordinates(x, y))
            ]
            
            if empty_coords:
                spawn_pos = empty_coords[randint(0, len(empty_coords) - 1)]
                grass = Grass(spawn_pos)
                board.set_piece(spawn_pos, grass) 