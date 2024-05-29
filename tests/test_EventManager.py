from src.game.constants.GameState import GameState
from src.game.constants.PlayerAction import PlayerAction
from src.game.constants.UnitAction import UnitAction
from src.game.engines.GameEngine import GameEngine
from src.game.engines.RenderEngine import RenderEngine
from src.game.maps.Map import Map
from src.game.managers.StateManager import GameStateManager


def setup_test_environment():
    game_world = Map.select_map("map1")
    screen_size = (500, 500)
    tile_size = 50
    state_manager = GameStateManager()
    state_manager.set_state(GameState.RUNNING)
    game_render = RenderEngine(game_world, screen_size, tile_size, state_manager)
    game_engine = GameEngine(game_world, game_render, state_manager)
    return game_engine


def test_valid_action_for_unit_creation():
    game_engine = setup_test_environment()
    # Create two worker units
    actions = [
        [
            PlayerAction.CREATE_WORKER
        ],
        [
            PlayerAction.CREATE_WORKER
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert len(game_engine.game_world.player_manager.players[0].units) == 1
    assert len(game_engine.game_world.player_manager.players[1].units) == 1

    # Don't move units
    # Create two infantry units
    actions = [
        [
            UnitAction.STAND,
            PlayerAction.CREATE_INFANTRY
        ],
        [
            UnitAction.STAND,
            PlayerAction.CREATE_INFANTRY
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert len(game_engine.game_world.player_manager.players[0].units) == 2
    assert len(game_engine.game_world.player_manager.players[1].units) == 2

    # Do nothing
    actions = [
        [
            UnitAction.STAND,
            UnitAction.STAND,
            PlayerAction.SKIP
        ],
        [
            UnitAction.STAND,
            UnitAction.STAND,
            PlayerAction.SKIP
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert len(game_engine.game_world.player_manager.players[0].units) == 2
    assert len(game_engine.game_world.player_manager.players[1].units) == 2


def test_valid_action_for_moving_units():
    game_engine = setup_test_environment()

    # Create two worker units
    actions = [
        [
            PlayerAction.CREATE_WORKER
        ],
        [
            PlayerAction.CREATE_WORKER
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert game_engine.game_world.get_tile((1, 0)).game_object == game_engine.game_world.player_manager.players[0].units.get(1)
    assert game_engine.game_world.get_tile((8, 9)).game_object == game_engine.game_world.player_manager.players[1].units.get(1)

    actions = [
        [
            UnitAction.DOWN,  # Move worker unit down for player 1
            PlayerAction.CREATE_WORKER  # Create another worker unit for player 1
        ],
        [
            UnitAction.UP,  # Move worker unit up for player 2
            PlayerAction.CREATE_WORKER  # Create another worker unit for player 2
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert game_engine.game_world.get_tile((2, 0)).game_object == game_engine.game_world.player_manager.players[0].units.get(1)
    assert game_engine.game_world.get_tile((7, 9)).game_object == game_engine.game_world.player_manager.players[1].units.get(1)
    assert game_engine.game_world.get_tile((1, 0)).game_object == game_engine.game_world.player_manager.players[0].units.get(2)
    assert game_engine.game_world.get_tile((8, 9)).game_object == game_engine.game_world.player_manager.players[1].units.get(2)

    actions = [
        [
            UnitAction.RIGHT,  # Move worker unit 1 right for player 1
            UnitAction.DOWN,  # Move worker unit 2 down for player 1
            PlayerAction.SKIP  # Do nothing for player 1
        ],
        [
            UnitAction.LEFT,  # Move worker unit 1 left for player 2
            UnitAction.UP,  # Move worker unit 2 down for player 2
            PlayerAction.SKIP  # Do nothing for player 2
        ]
    ]

    game_engine.event_manager.handle_ai(actions)

    assert game_engine.game_world.get_tile((2, 1)).game_object == game_engine.game_world.player_manager.players[0].units.get(1)
    assert game_engine.game_world.get_tile((7, 8)).game_object == game_engine.game_world.player_manager.players[1].units.get(1)
    assert game_engine.game_world.get_tile((2, 0)).game_object == game_engine.game_world.player_manager.players[0].units.get(2)
    assert game_engine.game_world.get_tile((7, 9)).game_object == game_engine.game_world.player_manager.players[1].units.get(2)
