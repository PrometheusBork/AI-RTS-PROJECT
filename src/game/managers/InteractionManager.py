from src.game.units.Unit import Unit
from src.game.objects.Base import Base
from src.game.interfaces.IAttacker import IAttacker
from src.game.interfaces.ICollector import ICollector
from src.game.interfaces.IAttackable import IAttackable
from src.game.interfaces.ICollectable import ICollectable


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
        attacker_player = self.player_manager.get_player_by_unit(movable_object)
        target_player = self.player_manager.get_player_by_unit(target_object) or self.player_manager.get_player_by_base(target_object)

        if attacker_player == target_player:
            return

        movable_object.attack(target_object)
        if not target_object.is_destroyed():
            return

        self.game_world.remove_game_object(target_position)

        if target_player:
            target_player.remove_unit(target_object)
            if isinstance(target_object, Base):
                attacker_player.bases_destroyed += 1

        if attacker_player and isinstance(target_object, Unit):
            attacker_player.units_destroyed += 1

    def reset(self, game_world):
        self.game_world = game_world
        self.player_manager = game_world.player_manager
