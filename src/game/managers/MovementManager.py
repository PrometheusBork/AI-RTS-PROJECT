from game.interfaces.IMoveable import IMovable
from game.interfaces.IObserveable import IObserveable
from game.interfaces.IObserver import IObserver
from game.managers.InteractionManager import InteractionManager
from game.constants.Direction import Direction


class MovementManager(IObserver):
    def __init__(self, game_world):
        self.game_world = game_world
        self.interaction_manager = InteractionManager(game_world)
        self.movable_objects = set()

    def register_movable_objects(self):
        for row in self.game_world.map:
            for tile in row:
                if not tile.is_empty():
                    self.add_moveable_object(tile.game_object)

    def add_moveable_object(self, moveable_object):
        if isinstance(moveable_object, IMovable):
            self.movable_objects.add(moveable_object)
            if isinstance(moveable_object, IObserveable):
                moveable_object.register(self)

    def remove_moveable_object(self, moveable_object):
        if moveable_object in self.movable_objects:
            self.movable_objects.remove(moveable_object)

    def move_objects(self, direction):
        for movable_object in self.movable_objects:
            current_position = movable_object.get_position()
            new_position = self.calculate_new_position(current_position, direction)

            if self.is_valid_move(new_position):
                self.handle_valid_move(movable_object, new_position)
            elif not self.is_position_out_of_bounds(new_position):
                self.interaction_manager.handle_interaction(movable_object, new_position)

    def move_object(self, movable_object, direction):
        if movable_object in self.movable_objects:
            current_position = movable_object.get_position()
            new_position = self.calculate_new_position(current_position, direction)
            
            if self.is_valid_move(new_position):
                self.handle_valid_move(movable_object, new_position)
            elif not self.is_position_out_of_bounds(new_position):
                self.interaction_manager.handle_interaction(movable_object, new_position)

    def calculate_new_position(self, current_position, direction):
        row, col = current_position
        if direction == Direction.UP:
            return row - 1, col
        elif direction == Direction.DOWN:
            return row + 1, col
        elif direction == Direction.LEFT:
            return row, col - 1
        elif direction == Direction.RIGHT:
            return row, col + 1
        else:
            return row, col

    def handle_valid_move(self, movable_object, new_position):
        current_position = movable_object.get_position()
        movable_object.update_position(new_position)
        self.game_world.get_tile(current_position).remove_placeable_object()
        self.game_world.get_tile(new_position).add_placeable_object(movable_object)

    def is_valid_move(self, new_position):
        return (
            not self.is_position_out_of_bounds(new_position)
            and self.is_position_empty(new_position)
            and self.is_position_walkable(new_position)
        )

    def is_position_out_of_bounds(self, position):
        row, col = position
        return (
                row < 0
                or col < 0
                or row >= self.game_world.grid_size[0]
                or col >= self.game_world.grid_size[1]
        )

    def is_position_empty(self, position):
        return self.game_world.get_tile(position).is_empty()

    def is_position_walkable(self, position):
        return self.game_world.get_tile(position).is_walkable

    def update(self, moveable_object):
        if moveable_object in self.movable_objects:
            self.remove_moveable_object(moveable_object)
