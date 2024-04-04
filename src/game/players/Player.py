from game.objects.Base import Base


class Player:
    def __init__(self, starting_resources, base):
        self.units = []
        self.resources = starting_resources
        self.base = base
        
    def lose(self):
        if self.base.is_destroyed():
            return True
    
    def add_unit(self, unit):
        self.units.append(unit)
        
    def remove_unit(self, unit):
        self.units.remove(unit)
        
    def add_resources(self, amount):
        self.resources += amount
        print(f"Player resources: {self.resources}")