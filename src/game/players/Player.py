class Player:
    def __init__(self, starting_resources, base):
        self.units = set()
        self.resources = starting_resources
        self.base = base

    def lose(self):
        return self.base.is_destroyed()

    def add_unit(self, unit):
        self.units.add(unit)

    def remove_unit(self, unit):
        self.units.discard(unit)

    def add_resources(self, amount):
        self.resources += amount
        
    def get_base_position(self):
        return self.base.row, self.base.col
