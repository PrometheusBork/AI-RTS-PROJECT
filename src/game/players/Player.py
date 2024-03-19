from game.objects.Base import Base


class Player:
    def __init__(self, units, resources, base: Base):
        self.units = units
        self.resources = resources # Needs to be implemented
        self.base = base
        
    def lose(self):
        if self.base.is_destroyed():
            return True
        