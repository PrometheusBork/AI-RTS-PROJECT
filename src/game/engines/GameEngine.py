import pygame

from game.constants.GameState import GameState
from game.managers.MovementManager import MovementManager
from game.managers.SelectionManager import SelectionManager
from game.constants.GlobalSettings import RESOURCE_TICK
from game.units.InfantryUnit import InfantryUnit
from game.units.WorkerUnit import WorkerUnit
from game.maps.Map import Map



class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.state_manager = state_manager
        self.state_manager.register(self.game_render)
        self.movement_manager = MovementManager(game_world)
        self.selection_manager = SelectionManager(game_world)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
        self.players = game_world.player_manager.players
    
    def run(self):
        self.selection_manager.register_selectable_objects()
        self.movement_manager.register_movable_objects()
        while self.state_manager.state != GameState.QUIT:
            self.render()
            self.clock.tick(60)
            if self.state_manager.state == GameState.RUNNING:
                self.check_game_over()
                self.resource_time += RESOURCE_TICK
                if self.resource_time >= 4:
                    for player in self.players:
                        player.add_resources(1)
                    self.resource_time = 0
            self.handle_events()
        self.game_render.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.set_state(GameState.QUIT)
            if self.selection_manager.get_selected_object() is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.handle_movement(self.selection_manager.get_selected_object(), "up")
                    if event.key == pygame.K_DOWN:
                        self.handle_movement(self.selection_manager.get_selected_object(), "down")
                    if event.key == pygame.K_LEFT:
                        self.handle_movement(self.selection_manager.get_selected_object(), "left")
                    if event.key == pygame.K_RIGHT:
                        self.handle_movement(self.selection_manager.get_selected_object(), "right")
                    if event.key == pygame.K_i:
                        if self.selection_manager.get_selected_object() == self.game_world.player_manager.players[0].base:
                            self.handle_unit_creation(self.game_world.player_manager.players[0], InfantryUnit(), 50)
                        elif self.selection_manager.get_selected_object() == self.game_world.player_manager.players[1].base:
                            self.handle_unit_creation(self.game_world.player_manager.players[1], InfantryUnit(), 50)
                    if event.key == pygame.K_w:
                        if self.selection_manager.get_selected_object() == self.game_world.player_manager.players[0].base:
                            self.handle_unit_creation(self.game_world.player_manager.players[0], WorkerUnit(), 25)
                        elif self.selection_manager.get_selected_object() == self.game_world.player_manager.players[1].base:
                            self.handle_unit_creation(self.game_world.player_manager.players[1], WorkerUnit(), 25)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state_manager.set_state(GameState.QUIT)
                if event.key == pygame.K_p:
                    self.state_manager.toggle_pause()
            if self.state_manager.state == GameState.MENU:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.game_render.menu_renderer.gui_manager.process_events(event)    
            if self.state_manager.state == GameState.RUNNING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_selection(self.selection_manager.is_hovered(mouse_pos=pygame.mouse.get_pos()))

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

    def check_game_over(self):
        for player in self.players:
            if player.base.is_destroyed():
                self.state_manager.set_state(GameState.MENU)
                
                return print(f"Player {player} has lost the game!")
    
    def render(self):
        self.game_render.render()
