import pygame

from src.game.managers.SelectionManager import SelectionManager
from src.game.managers.MovementManager import MovementManager
from src.game.constants.GameState import GameState
from src.game.units.InfantryUnit import InfantryUnit
from src.game.units.WorkerUnit import WorkerUnit
from src.game.constants.UnitAction import UnitAction
from src.game.constants.PlayerAction import PlayerAction


class EventManager:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        self.movement_manager = MovementManager(game_world)
        self.selection_manager = SelectionManager(game_world)
        self.players = game_world.player_manager.players

    def handle_events(self):
        for event in pygame.event.get():  
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseclick(event)
            if event.type == pygame.QUIT:
                self.state_manager.set_state(GameState.QUIT)

    def handle_ai(self, actions):
        for player_index, player_actions in enumerate(actions):
            player = self.players[player_index]

            # Iterate over units and actions
            for unit_index, unit_level_action in enumerate(player_actions[:-1]):
                unit = player.units.get(unit_index + 1)

                if unit_level_action == UnitAction.STAND:  # Skip action
                    continue
                elif unit_level_action in [UnitAction.UP, UnitAction.DOWN, UnitAction.LEFT, UnitAction.RIGHT]:
                    self.handle_unit_movement(unit, unit_level_action)
                else:
                    raise ValueError(f"Invalid action: {unit_level_action}")

            # Handle player-level actions
            player_level_action = player_actions[-1]
            if player_level_action == PlayerAction.SKIP:  # Skip action
                continue
            elif player_level_action == PlayerAction.CREATE_INFANTRY:
                self.handle_unit_creation(player, InfantryUnit(), 50)
            elif player_level_action == PlayerAction.CREATE_WORKER:
                self.handle_unit_creation(player, WorkerUnit(), 25)
            else:
                raise ValueError(f"Invalid action: {player_level_action}")

    def handle_mouseclick(self, event):
        if self.state_manager.state == GameState.RUNNING:
            self.handle_selection(self.selection_manager.is_hovered(mouse_pos=pygame.mouse.get_pos()))
        elif self.state_manager.state == GameState.MENU:
            self.game_render.menu_renderer.gui_manager.process_events(event)

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.state_manager.set_state(GameState.QUIT)

        if self.state_manager.state == GameState.RUNNING or self.state_manager.state == GameState.PAUSED:
            if key == pygame.K_p:
                self.state_manager.toggle_pause()

        if self.state_manager.state != GameState.RUNNING:
            return

        selected_object = self.selection_manager.get_selected_object()
        if selected_object is None:
            return

        for player in self.players:
            if selected_object in player.units.values() or selected_object == player.base:
                if key == pygame.K_UP:
                    self.handle_unit_movement(selected_object, UnitAction.UP)
                if key == pygame.K_DOWN:
                    self.handle_unit_movement(selected_object, UnitAction.DOWN)
                if key == pygame.K_LEFT:
                    self.handle_unit_movement(selected_object, UnitAction.LEFT)
                if key == pygame.K_RIGHT:
                    self.handle_unit_movement(selected_object, UnitAction.RIGHT)
                if key == pygame.K_i:
                    self.handle_unit_creation(player, InfantryUnit(), 50)
                if key == pygame.K_w:
                    self.handle_unit_creation(player, WorkerUnit(), 25)
                break
    
    def handle_unit_movement(self, movable_object, direction):
        if self.state_manager.state == GameState.RUNNING:
            self.movement_manager.move_object(movable_object, direction)

    def handle_selection(self, mouse_pos):
        if self.state_manager.state == GameState.RUNNING:
            self.selection_manager.select_object(mouse_pos)
            
    def handle_unit_creation(self, player, unit, cost):
        valid_position = self.search_valid_unit_position(player)
        if player.resources >= cost and valid_position:
            player.resources -= cost
            player.add_unit(unit)
            self.game_world.set_game_object(valid_position, unit)
            self.game_render.hover_renderer.add_hoverable_object(unit).sort_hoverable_objects()
            self.game_render.sprite_manager.add_sprite(unit).sort_sprite_groups()
            self.movement_manager.add_moveable_object(unit)
            self.selection_manager.add_selectable_object(unit)
    
    def search_valid_unit_position(self, player):
        base_position = player.base.row, player.base.col
        adjacent_positions = [(base_position[0] + 1, base_position[1]), (base_position[0] - 1, base_position[1]),
                              (base_position[0], base_position[1] + 1), (base_position[0], base_position[1] - 1), 
                              (base_position[0] + 1, base_position[1] + 1), (base_position[0] - 1, base_position[1] - 1), 
                              (base_position[0] + 1, base_position[1] - 1), (base_position[0] - 1, base_position[1] + 1)]
        for position in adjacent_positions:
            if not self.game_world.is_position_out_of_bounds(position) and self.game_world.get_tile(position).is_empty():
                return position
        return False

    def reset(self, game_world):
        self.game_world = game_world
        self.players = game_world.player_manager.players
        self.movement_manager.reset(game_world)
        self.selection_manager.reset(game_world)
