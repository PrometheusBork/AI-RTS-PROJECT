from interfaces.IMoveable import IMovable


class MovementManager:
    def __init__(self, game_world):
        self.game_world = game_world
        self.movable_objects = []

    def register_movable_object(self, movable_object):
        if isinstance(movable_object, IMovable):
            self.movable_objects.append(movable_object)

    def move_object(self, movable_object, direction):
        if movable_object in self.movable_objects:
            current_position = movable_object.get_position()
            new_position = self.calculate_new_position(current_position, direction)

            if self.is_valid_move(new_position):
                movable_object.update_position(new_position)
            else:
                print(f"Cannot move {movable_object} to {new_position}")

    def calculate_new_position(self, current_position, direction):
        row, col = current_position
        if direction == "up":
            return row - 1, col
        elif direction == "down":
            return row + 1, col
        elif direction == "left":
            return row, col - 1
        elif direction == "right":
            return row, col + 1
        else:
            return row, col

    def is_valid_move(self, new_position):
        pass
