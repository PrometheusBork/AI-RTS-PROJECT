from game.engines.GameEngine import GameEngine
from game.engines.RenderEngine import RenderEngine
from game.managers.StateManager import GameStateManager
from game.maps.Map import Map
from ai.envs.GameEnv import GameEnv
from ai.agents.DQL import DQL


def main():
    grid_size = (10, 10) # We should find a way to get the Grid Size from the Map file
    tile_size = 50
    screen_size = (grid_size[0] * tile_size + (2 * tile_size) + 200, grid_size[1] * tile_size + (2 * tile_size))

    # Create a GameWorld instance
    game_world = Map.select_map("map1")

    # Create Game State manager instance
    state_manager = GameStateManager()

    # Create Game Render instance
    game_render = RenderEngine(game_world, screen_size, tile_size, state_manager)

    # Create Game Engine instance
    game_engine = GameEngine(game_world, game_render, state_manager)

    # Create Game Environment instance
    game_env = GameEnv(game_engine, game_render)

    players = game_world.player_manager.players

    agent1 = DQL(players[0], 1, 2)
    agent2 = DQL(players[1], 1, 2)

    agents = [agent1, agent2]

    num_episodes = 100
    for episode in range(num_episodes):
        state = game_env.reset() if episode != 0 else None
        terminated = False
        while not terminated:
            actions = (agent.act(state) for agent in agents)
            next_states, rewards, terminated, truncated, info = game_env.step(actions)
            state = next_states


if __name__ == "__main__":
    main()
