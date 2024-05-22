import gym
import numpy as np
from gym import spaces

from src.game.maps.Map import Map
from src.game.objects.Base import Base
from src.game.objects.Tree import Tree
from src.game.units.InfantryUnit import InfantryUnit
from src.game.units.WorkerUnit import WorkerUnit


class GameEnv(gym.Env):
    def __init__(self, game_engine, game_render, num_agents=1):
        super(GameEnv, self).__init__()
        self.game_engine = game_engine
        self.render_engine = game_render
        self.num_agents = num_agents
        self.object_encoding = {
            "empty": 1,
            "tree": 2,
            "base": 3,
            "worker": 4,
            "infantry": 5
        }

    def step(self, actions):
        self.game_engine.next_step(actions)
        self.render()

        observations = self._next_observation()
        rewards = [0.0] * self.num_agents
        terminated = self.game_engine.check_game_over()
        truncated = False
        info = {}

        return observations, rewards, terminated, truncated, info

    def _next_observation(self):
        rows, cols = self.game_engine.game_world.grid_size[0], self.game_engine.game_world.grid_size[1]
        tile_channel = np.zeros((rows, cols), dtype=np.int32)
        player_channel = np.zeros((rows, cols), dtype=np.int32)

        for row in range(rows):
            for col in range(cols):
                tile = self.game_engine.game_world.get_tile((row, col))

                if tile.is_walkable and tile.is_empty():
                    tile_channel[row, col] = self.object_encoding["empty"]
                elif isinstance(tile.game_object, Tree):
                    tile_channel[row, col] = self.object_encoding["tree"]
                elif isinstance(tile.game_object, Base):
                    tile_channel[row, col] = self.object_encoding["base"]
                elif isinstance(tile.game_object, WorkerUnit):
                    tile_channel[row, col] = self.object_encoding["worker"]
                elif isinstance(tile.game_object, InfantryUnit):
                    tile_channel[row, col] = self.object_encoding["infantry"]

        for player_index in range(self.num_agents):
            player = self.game_engine.game_world.player_manager.players[player_index]
            base_pos = player.get_base_position()
            tile_with_base = self.game_engine.game_world.get_tile(base_pos)
            if not tile_with_base.is_empty():
                player_channel[base_pos[0], base_pos[1]] = 1000 * (player_index + 1)

            for index, unit in player.units.items():
                player_channel[unit.row, unit.col] = 1000 * (player_index + 1) + index

        return np.stack((tile_channel, player_channel), axis=2)

    def render(self):
        self.game_engine.render()

    def reset(self, seed=None, options=None):
        new_game = Map.select_map("map1")
        self.game_engine.reset(new_game)
        self.render()
        return self._next_observation()

    def close(self):
        self.game_engine.quit()
