import numpy as np
import pygame

from game.constants.GameState import GameState
from game.managers.EventManager import EventManager
from game.constants.GlobalSettings import RESOURCE_TICK
from game.objects.Base import Base
from game.objects.Tree import Tree
from game.units.InfantryUnit import InfantryUnit
from game.units.WorkerUnit import WorkerUnit



class GameEngine:
    def __init__(self, game_world, game_render, state_manager):
        self.game_world = game_world
        self.game_render = game_render
        self.game_render.menu_renderer.register(state_manager)
        self.state_manager = state_manager
        state_manager.register(game_render)
        self.event_manager = EventManager(game_world, game_render, state_manager)
        self.clock = pygame.time.Clock()
        self.resource_time = 0
        self.object_encoding = {
            "empty": 1,
            "tree": 2,
            "base": 3,
            "worker": 4,
            "infantry": 5
        }
        self.player_encoding = {
            0: range(100, 199),
            1: range(200, 299),
            2: range(300, 399),
            3: range(400, 499) 
        }
    
    def run(self):
        while self.state_manager.state != GameState.QUIT:
            self.next_step(None)
            self.render()
            return "break"
        self.quit()

    def next_step(self, actions):
        self.event_manager.handle_events()
        if self.state_manager.state == GameState.RUNNING:
            self.event_manager.handle_ai(actions)
            self.resource_time += RESOURCE_TICK
            if self.resource_time >= 4:
                for player in self.game_world.player_manager.players:
                    player.add_resources(10)
                print("Resources:", [player.resources for player in self.game_world.player_manager.players])
                self.resource_time = 0
        self.clock.tick(60)

    def check_game_over(self):
        for player in self.game_world.player_manager.players:
            if player.base.is_destroyed():
                print(f"Player {player} has lost the game!")
                return True
        return False

    def get_observation_space(self):
        observation = []
        for row in self.game_world.map:
            for tile in row:
                self.observe_space(tile, observation)
        return observation
    
    def observe_space(self, tile, observation):
        if tile.is_walkable and tile.is_empty():
            observation.append(tuple([None, 1]))
        elif isinstance(tile.game_object, Tree):
            observation.append(tuple([None, 2]))
        elif isinstance(tile.game_object, WorkerUnit):
            observation.append(tuple([self.game_world.player_manager.get_player_by_unit(tile.game_object), 3]))
        elif isinstance(tile.game_object, InfantryUnit):
            observation.append(tuple([self.game_world.player_manager.get_player_by_unit(tile.game_object), 4]))
        elif isinstance(tile.game_object, Base):
            observation.append(tuple([self.game_world.player_manager.get_player_by_base(tile.game_object), 5]))
        else:
            observation.append(tuple([None, 0]))
    
    def get_observation_space2(self):
        rows, cols = self.game_world.grid_size[0], self.game_world.grid_size[1]
        tile_channel = np.zeros((rows, cols), dtype=np.int32)
        unit_channel = np.zeros((rows, cols), dtype=np.int32)

        # Initialize used indices dictionary and reserve the first index for the base
        used_indices = {i: set() for i in range(len(self.game_world.player_manager.players))}
        base_indices = {i: next(iter(self.player_encoding[i])) for i in range(len(self.game_world.player_manager.players))}

        # Pre-assign the base index in unit_channel and mark it as used
        for player_index, player in enumerate(self.game_world.player_manager.players):
            base_pos = player.get_base_position()
            unit_channel[base_pos[0], base_pos[1]] = base_indices[player_index]
            used_indices[player_index].add(base_indices[player_index])
            
        for row in range(rows):
            for col in range(cols):
                tile = self.game_world.get_tile((row, col))
                # Populate tile_channel based on the type of the object
                if tile.is_walkable and tile.is_empty():
                    tile_channel[row][col] = self.object_encoding["empty"]
                elif isinstance(tile.game_object, Tree):
                    tile_channel[row][col] = self.object_encoding["tree"]
                elif isinstance(tile.game_object, Base):
                    tile_channel[row][col] = self.object_encoding["base"]
                elif isinstance(tile.game_object, WorkerUnit):
                    tile_channel[row][col] = self.object_encoding["worker"]
                elif isinstance(tile.game_object, InfantryUnit):
                    tile_channel[row][col] = self.object_encoding["infantry"]
                # Assign indices to other units
                for player_index, player in enumerate(self.game_world.player_manager.players):
                    if tile.game_object in player.units:
                        # Start with the second index since the first is reserved for the base
                        for index in self.player_encoding[player_index]:
                            if index not in used_indices[player_index]:
                                unit_channel[row][col] = index
                                used_indices[player_index].add(index)
                                break

        channel = np.stack((tile_channel, unit_channel), axis=-1)
        print(channel)  # Print the final channel array
        return channel
        
    
    def reset(self, game_world):
        self.game_world = game_world
        self.state_manager.set_state(GameState.RUNNING)
        self.event_manager.reset(game_world)
        self.game_render.reset(game_world)
        self.resource_time = 0

    def render(self):
        self.game_render.render()

    def quit(self):
        self.game_render.quit()
