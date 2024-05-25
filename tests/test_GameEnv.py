import tensorflow as tf

from src.game.engines.GameEngine import GameEngine
from src.game.engines.RenderEngine import RenderEngine
from src.ai.envs.GameEnv import GameEnv
from src.game.maps.Map import Map
from src.game.managers.StateManager import GameStateManager


def setup_test_environment():
    game_world = Map.select_map("map1")
    screen_size = (500, 500)
    tile_size = 50
    num_agents = 2
    state_manager = GameStateManager()
    game_render = RenderEngine(game_world, screen_size, tile_size, state_manager)
    game_engine = GameEngine(game_world, game_render, state_manager)
    game_env = GameEnv(game_engine, game_render, num_agents)
    return game_env, num_agents


def test_executes_next_step():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    game_env.step(actions)
    assert game_env.game_engine.next_step, "next_step method should be called"


def test_returns_rewards_as_zeros():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    _, rewards, _, _, _ = game_env.step(actions)
    assert rewards == [0.0] * num_agents, "rewards should be a list of zeros"


def test_sets_truncated_to_false():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    observations, rewards, terminated, truncated, info = game_env.step(actions)
    assert not truncated, "truncated should be set to False"


def test_sets_info_to_empty_dict():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    _, _, _, _, info = game_env.step(actions)
    assert info == {}, "info should be an empty dictionary"


def test_returns_observations_as_result_of_next_observation():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    observations, _, _, _, _ = game_env.step(actions)
    tf.debugging.assert_equal(tf.reduce_all(tf.equal(observations, game_env._next_observation())), True, "observations should be the result of calling _next_observation")


def test_sets_terminated_to_result_of_check_game_over():
    game_env, num_agents = setup_test_environment()
    actions = [0] * num_agents
    _, _, terminated, _, _ = game_env.step(actions)
    assert terminated == game_env.game_engine.check_game_over(), "terminated should be set to the result of calling check_game_over on game_engine"


def test_observation_shape():
    game_env, _ = setup_test_environment()
    observation = game_env._next_observation()

    assert isinstance(observation, tf.Tensor), 'Observation should be a TensorFlow array'

    """Test that observation has the correct shape
    Correct shape is (10, 10, 2)"""
    assert observation.shape == (game_env.game_engine.game_world.grid_size[0], game_env.game_engine.game_world.grid_size[1], 2), "Observation should have the correct shape"


def test_observation_with_bases():
    game_env, _ = setup_test_environment()
    observation = game_env._next_observation()

    base_positions = [(0, 0), (9, 9)]
    for i, base_position in enumerate(base_positions):
        base_index = 1000 * (i + 1)

        tile_observation = observation[base_position[0], base_position[1], 0]
        player_observation = observation[base_position[0], base_position[1], 1]
        assert tile_observation == game_env.object_encoding["base"], f'Observation should contain the base object encoding: {game_env.object_encoding["base"]}'
        assert player_observation == base_index, f'Observation should contain the player index {base_index}'


def test_observation_with_no_objects():
    game_env, _ = setup_test_environment()
    game_env.game_engine.game_world.clear_objects()
    observation = game_env._next_observation()

    tf.debugging.assert_equal(tf.reduce_all(observation[:, :, 1] == 0), True, 'Observation should contain only zeros when there are no objects')
    tf.debugging.assert_equal(tf.reduce_all(tf.math.logical_or(observation[:, :, 0] == 0, observation[:, :, 0] == 1)), True, 'Observation should only be encoded with 0 or 1')
