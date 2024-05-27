import heapq


class Player:
    def __init__(self, starting_resources, base, color):
        self.color = color
        self.units = dict()
        self.available_indices = []
        heapq.heappush(self.available_indices, 1)
        self.resources = starting_resources
        self.base = base
        self.units_created = 0
        self.units_destroyed = 0
        self.units_lost = 0
        self.resources_collected = 0

    def lose(self):
        return self.base.is_destroyed()

    def add_unit(self, unit):
        if self.color.value is not None:
            unit.color_image.fill(self.color.value)
            unit.set_color()
        if unit not in self.units.values():
            if self.available_indices:
                min_index = heapq.heappop(self.available_indices)
            else:
                max_index = max(self.units.keys(), default=0)
                min_index = max_index + 1
                heapq.heappush(self.available_indices, min_index + 1)
            self.units[min_index] = unit
            self.units_created += 1

    def remove_unit(self, unit):
        for index, u in self.units.items():
            if u == unit:
                del self.units[index]
                heapq.heappush(self.available_indices, index)
                self.units_lost += 1
                break

    def add_resources(self, amount):
        self.resources += amount
        self.resources_collected += amount
        
    def get_base_position(self):
        return self.base.row, self.base.col

    def get_unit_index(self, unit):
        for index, u in self.units.items():
            if u == unit:
                return index
        return 0
