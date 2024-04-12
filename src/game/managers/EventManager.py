import pygame

from game.managers.SelectionManager import SelectionManager
from game.managers.MovementManager import MovementManager
from game.constants.GameState import GameState
from game.units.InfantryUnit import InfantryUnit
from game.units.WorkerUnit import WorkerUnit
from game.constants.Direction import Direction


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
            if selected_object in player.units or selected_object == player.base:
                if key == pygame.K_UP:
                    self.handle_movement(selected_object, Direction.UP)
                if key == pygame.K_DOWN:
                    self.handle_movement(selected_object, Direction.DOWN)
                if key == pygame.K_LEFT:
                    self.handle_movement(selected_object, Direction.LEFT)
                if key == pygame.K_RIGHT:
                    self.handle_movement(selected_object, Direction.RIGHT)
                if key == pygame.K_i:
                    self.handle_unit_creation(player, InfantryUnit(), 50)
                if key == pygame.K_w:
                    self.handle_unit_creation(player, WorkerUnit(), 25)
                break
    
    def handle_movement(self, movable_object, direction):
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