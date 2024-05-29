import tensorflow as tf
from gym import Env

from src.game.maps.Map import Map
from src.game.objects.Base import Base
from src.game.objects.Tree import Tree
from src.game.units.InfantryUnit import InfantryUnit
from src.game.units.WorkerUnit import WorkerUnit


class GameEnv(Env):
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
        rewards = self._calculate_rewards()
        terminated = self.game_engine.check_game_over()
        truncated = False
        info = {}

        return observations, rewards, terminated, truncated, info

    def get_player_stats(self):
        stats = []
        for player_index in range(self.num_agents):
            player = self.game_engine.game_world.player_manager.players[player_index]
            player_stats = {
                'units_created': player.units_created,
                'units_destroyed': player.units_destroyed,
                'units_lost': player.units_lost,
                'resources_collected': player.resources_collected,
                'bases_destroyed': player.bases_destroyed,
                'has_lost': player.lose()
            }
            stats.append(player_stats)
        return stats

    def _next_observation(self):
        rows, cols = self.game_engine.game_world.grid_size[0], self.game_engine.game_world.grid_size[1]
        tile_channel = tf.zeros((rows, cols), dtype=tf.int32)
        player_channel = tf.zeros((rows, cols), dtype=tf.int32)

        for row in range(rows):
            for col in range(cols):
                tile = self.game_engine.game_world.get_tile((row, col))

                if tile.is_walkable and tile.is_empty():
                    tile_channel = tf.tensor_scatter_nd_update(tile_channel, [[row, col]], [self.object_encoding["empty"]])
                elif isinstance(tile.game_object, Tree):
                    tile_channel = tf.tensor_scatter_nd_update(tile_channel, [[row, col]], [self.object_encoding["tree"]])
                elif isinstance(tile.game_object, Base):
                    tile_channel = tf.tensor_scatter_nd_update(tile_channel, [[row, col]], [self.object_encoding["base"]])
                elif isinstance(tile.game_object, WorkerUnit):
                    tile_channel = tf.tensor_scatter_nd_update(tile_channel, [[row, col]], [self.object_encoding["worker"]])
                elif isinstance(tile.game_object, InfantryUnit):
                    tile_channel = tf.tensor_scatter_nd_update(tile_channel, [[row, col]], [self.object_encoding["infantry"]])

        for player_index in range(self.num_agents):
            player = self.game_engine.game_world.player_manager.players[player_index]
            base_pos = player.get_base_position()
            tile_with_base = self.game_engine.game_world.get_tile(base_pos)
            if not tile_with_base.is_empty():
                player_channel = tf.tensor_scatter_nd_update(player_channel, [[base_pos[0], base_pos[1]]], [1000 * (player_index + 1)])

            for index, unit in player.units.items():
                player_channel = tf.tensor_scatter_nd_update(player_channel, [[unit.row, unit.col]], [1000 * (player_index + 1) + index])

        return tf.stack((tile_channel, player_channel), axis=2)

    def _calculate_rewards(self):
        player_stats = self.get_player_stats()
        rewards = [0.0] * self.num_agents

        for player_index, stats in enumerate(player_stats):
            # +100 for each enemy unit destroyed
            rewards[player_index] += stats['units_destroyed'] * 100

            # +1 for collecting resources
            rewards[player_index] += stats['resources_collected']

            # -5 for each unit lost
            rewards[player_index] -= stats['units_lost'] * 5

            # -1000 for losing the game
            if stats['has_lost']:
                rewards[player_index] -= 1000

            # +1000 for each enemy base destroyed
            rewards[player_index] += stats['bases_destroyed'] * 1000

        return rewards

    def render(self):
        self.game_engine.render()

    def reset(self, seed=None, options=None):
        new_game = Map.select_map("map1")
        self.game_engine.reset(new_game)
        self.render()
        return self._next_observation()

    def close(self):
        self.game_engine.quit()
