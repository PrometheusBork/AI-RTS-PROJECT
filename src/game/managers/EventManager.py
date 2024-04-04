import pygame

from game.managers.SelectionManager import SelectionManager
from game.managers.MovementManager import MovementManager
from game.constants.GameState import GameState
from game.units.InfantryUnit import InfantryUnit
from game.units.WorkerUnit import WorkerUnit

class EventManager:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        self.movement_manager = MovementManager(game_world)
        self.selection_manager = SelectionManager(game_world)
        self.players = game_world.player_manager.players
        
    
    def handle_events(self):
        self.selection_manager.register_selectable_objects()
        self.movement_manager.register_movable_objects()
        for event in pygame.event.get():  
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseclick(event)

    def handle_mouseclick(self, event):
        if self.state_manager.state == GameState.RUNNING:
            self.handle_selection(self.selection_manager.is_hovered(mouse_pos=pygame.mouse.get_pos()))
        elif self.state_manager.state == GameState.MENU:
            self.game_render.menu_renderer.gui_manager.process_events(event)

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
                self.state_manager.set_state(GameState.QUIT)
        if self.state_manager.state == GameState.RUNNING:
            if self.selection_manager.get_selected_object() is not None:
                if key == pygame.K_UP:
                    self.handle_movement(self.selection_manager.get_selected_object(), "up")
                if key == pygame.K_DOWN:
                    self.handle_movement(self.selection_manager.get_selected_object(), "down")
                if key == pygame.K_LEFT:
                    self.handle_movement(self.selection_manager.get_selected_object(), "left")
                if key == pygame.K_RIGHT:
                    self.handle_movement(self.selection_manager.get_selected_object(), "right")
                if key == pygame.K_i:
                    if self.selection_manager.get_selected_object() == self.game_world.player_manager.players[0].base:
                        self.handle_unit_creation(self.game_world.player_manager.players[0], InfantryUnit(), 50)
                    elif self.selection_manager.get_selected_object() == self.game_world.player_manager.players[1].base:
                        self.handle_unit_creation(self.game_world.player_manager.players[1], InfantryUnit(), 50)
                if key == pygame.K_w:
                    if self.selection_manager.get_selected_object() == self.game_world.player_manager.players[0].base:
                        self.handle_unit_creation(self.game_world.player_manager.players[0], WorkerUnit(), 25)
                    elif self.selection_manager.get_selected_object() == self.game_world.player_manager.players[1].base:
                        self.handle_unit_creation(self.game_world.player_manager.players[1], WorkerUnit(), 25)
        if self.state_manager.state == GameState.RUNNING or self.state_manager.state == GameState.PAUSED:
            if key == pygame.K_p:
                self.state_manager.toggle_pause()
    
    def handle_movement(self, movable_object, direction):
        if self.state_manager.state == GameState.RUNNING:
            self.movement_manager.move_object(movable_object, direction)

    def handle_selection(self, mouse_pos):
        if self.state_manager.state == GameState.RUNNING:
            self.selection_manager.select_object(mouse_pos)
            
    def handle_unit_creation(self, player, unit, cost):
        position = self.search_valid_unit_position(player)
        if player.resources >= cost and position:
            player.resources -= cost
            player.add_unit(unit)
            self.game_world.set_game_object(position, player.units[-1])
            self.game_render.hover_renderer.register_hoverable_objects()
            self.game_render.sprite_manager.register_sprite_groups()
            self.movement_manager.register_movable_objects()
            self.selection_manager.register_selectable_objects()        
    
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