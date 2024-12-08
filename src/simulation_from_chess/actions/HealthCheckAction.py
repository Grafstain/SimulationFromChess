from ..entities.Creature import Creature
from .Action import Action

class HealthCheckAction(Action):
    def execute(self, board, logger):
        """Проверяет здоровье существ и удаляет мёртвых."""
        entities_to_remove = []
        
        for coordinates, entity in board.entities.items():
            if isinstance(entity, Creature) and entity.hp <= 0:
                entities_to_remove.append(coordinates)
                logger.log_action(entity, "Погиб", f"на координатах ({coordinates.x}, {coordinates.y})")
                
        for coordinates in entities_to_remove:
            board.remove_piece(coordinates) 