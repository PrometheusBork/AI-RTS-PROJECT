import heapq


class Player:
    def __init__(self, starting_resources, base):
        self.units = dict()
        self.available_indices = []
        heapq.heappush(self.available_indices, 1)
        self.resources = starting_resources
        self.base = base

    def lose(self):
        return self.base.is_destroyed()

    def add_unit(self, unit):
        if unit not in self.units.values():
            if self.available_indices:
                min_index = heapq.heappop(self.available_indices)
            else:
                max_index = max(self.units.keys(), default=0)
                min_index = max_index + 1
                heapq.heappush(self.available_indices, min_index + 1)
            self.units[min_index] = unit

    def remove_unit(self, unit):
        for index, u in self.units.items():
            if u == unit:
                del self.units[index]
                heapq.heappush(self.available_indices, index)
                break

    def add_resources(self, amount):
        self.resources += amount
        
    def get_base_position(self):
        return self.base.row, self.base.col

    def get_unit_index(self, unit):
        for index, u in self.units.items():
            if u == unit:
                return index
        return 0
