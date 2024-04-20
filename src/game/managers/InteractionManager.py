from game.interfaces.IAttacker import IAttacker
from game.interfaces.ICollector import ICollector
from game.interfaces.IAttackable import IAttackable
from game.interfaces.ICollectable import ICollectable


class InteractionManager:
    def __init__(self, game_world):
        self.game_world = game_world
        self.player_manager = game_world.player_manager

    def handle_interaction(self, movable_object, target_position):
        target_object = self.game_world.get_tile(target_position).game_object

        if isinstance(movable_object, ICollector) and isinstance(target_object, ICollectable):
            self.handle_collectable_interaction(movable_object, target_object, target_position)
        elif isinstance(movable_object, IAttacker) and isinstance(target_object, IAttackable):
            self.handle_attackable_interaction(movable_object, target_object, target_position)

    def handle_collectable_interaction(self, movable_object, collectable_object, target_position):
        resources_collected = movable_object.collect(collectable_object)
        player = self.player_manager.get_player_by_unit(movable_object)
        if player:
            player.add_resources(resources_collected)
        if collectable_object.is_destroyed():
            self.game_world.remove_game_object(target_position)

    def handle_attackable_interaction(self, movable_object, target_object, target_position):
        if self.player_manager.get_player_by_unit(movable_object) != (self.player_manager.get_player_by_unit(target_object) or self.player_manager.get_player_by_base(target_object)):
            movable_object.attack(target_object)
            if target_object.is_destroyed():
                self.game_world.remove_game_object(target_position)
                player = self.player_manager.get_player_by_unit(target_object)
                if player:
                    player.remove_unit(target_object)

    def reset(self, game_world):
        self.game_world = game_world
        self.player_manager = game_world.player_manager
