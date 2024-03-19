from game.units.InfantryUnit import InfantryUnit
from game.units.WorkerUnit import WorkerUnit
from game.objects.Base import Base


class Player:
    def __init__(self, user, units, resources, base: Base):
        self.user = user
        self.units = units
        self.resources = resources # Needs to be implemented
        self.base = base
        
    def lose(self):
        if self.base.is_destroyed():
            return True
        