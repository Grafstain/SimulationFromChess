from ..entities.Creature import Creature
from .Action import Action

class HealthCheckAction(Action):
    def execute(self, board):
        """Проверяет здоровье существ и удаляет мёртвых."""
        entities_to_remove = []
        
        for coordinates, entity in board.entities.items():
            if isinstance(entity, Creature) and entity.hp <= 0:
                entities_to_remove.append(coordinates)
                
        for coordinates in entities_to_remove:
            entity = board.get_piece(coordinates)
            board.remove_piece(coordinates)
            print(f"{entity} на {coordinates} погиб") 