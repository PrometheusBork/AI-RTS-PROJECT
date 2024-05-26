import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, GRU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Model

from src.game.constants.PlayerAction import PlayerAction
from src.game.constants.UnitAction import UnitAction
from src.ai.utils import get_num_units
from src.ai.replay_buffer import ReplayBuffer
from src.game.engines.GameEngine import GameEngine
from src.game.engines.RenderEngine import RenderEngine
from src.game.managers.StateManager import GameStateManager
from src.game.maps.Map import Map
from src.ai.envs.GameEnv import GameEnv


class QNetwork(Model):
    def __init__(self, unit_action_space, player_action_space):
        super(QNetwork, self).__init__()
        self.initial_state = tf.zeros((1, 64))
        self.unit_action_space = unit_action_space
        self.player_action_space = player_action_space

        self.conv1 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')
        self.pool1 = MaxPooling2D((2, 2))
        self.conv2 = Conv2D(32, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')
        self.pool2 = MaxPooling2D((2, 2))
        self.flatten = Flatten()
        self.dense1 = Dense(64, activation='relu', kernel_initializer='he_normal')

        self.unit_rnn = GRU(32, return_sequences=True, return_state=True, kernel_initializer='he_normal')
        self.unit_dense = Dense(unit_action_space, activation='linear', kernel_initializer='he_normal')
        self.player_dense = Dense(player_action_space, activation='linear', kernel_initializer='he_normal')

    def call(self, inputs, unit_sequences):
        x = self.conv1(inputs)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.flatten(x)
        x = self.dense1(x)

        batch_size = tf.shape(inputs)[0]
        initial_state = tf.zeros((batch_size, 32))

        if unit_sequences.shape[1] > 0:
            unit_q_values, _ = self.unit_rnn(unit_sequences, initial_state=initial_state)
            unit_q_values = self.unit_dense(unit_q_values)
        else:
            unit_q_values = tf.zeros((batch_size, 0, self.unit_action_space))

        player_q_values = self.player_dense(x)

        return unit_q_values, player_q_values


def train_agent(q_network, target_q_network, optimizer, experiences, agent_id):
    states, actions, rewards, next_states, terminates = zip(*experiences)

    states = tf.convert_to_tensor(states, dtype=tf.float32)
    next_states = tf.convert_to_tensor(next_states, dtype=tf.float32)
    rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)
    terminates = tf.convert_to_tensor(terminates, dtype=tf.float32)

    batch_size = states.shape[0]
    rewards = tf.reshape(rewards[:, agent_id], [batch_size])

    unit_sequences = create_unit_sequences(states, q_network, agent_id)
    next_unit_sequences = create_unit_sequences(next_states, q_network, agent_id)

    next_unit_q_values, next_player_q_values = target_q_network(next_states, unit_sequences=next_unit_sequences)
    max_next_unit_q_values = tf.reduce_max(next_unit_q_values, axis=2)
    max_next_player_q_values = tf.reduce_max(next_player_q_values, axis=1)
    summed_max_next_unit_q_values = tf.reduce_sum(max_next_unit_q_values, axis=1)
    target_q_values = rewards + (1 - terminates) * 0.99 * (summed_max_next_unit_q_values + max_next_player_q_values)

    with tf.GradientTape() as tape:
        unit_q_values, player_q_values = q_network(states, unit_sequences=unit_sequences)

        agent_actions = extract_agent_actions(actions, agent_id)
        unit_actions, max_units = get_unit_actions(agent_actions)
        padded_unit_actions = pad_unit_actions(unit_actions, max_units)

        unit_actions_tensor = tf.convert_to_tensor(padded_unit_actions, dtype=tf.int32)
        player_actions = tf.convert_to_tensor([action[-1].value for action in agent_actions], dtype=tf.int32)

        one_hot_unit_actions = tf.one_hot(unit_actions_tensor, q_network.unit_action_space)
        one_hot_player_actions = tf.one_hot(player_actions, q_network.player_action_space)

        q_unit_values = tf.reduce_sum(unit_q_values * one_hot_unit_actions, axis=2)
        q_player_values = tf.reduce_sum(player_q_values * one_hot_player_actions, axis=1)
        q_values = tf.reduce_sum(q_unit_values, axis=1) + q_player_values
        target_q_values = tf.reshape(target_q_values, q_values.shape)
        loss = MeanSquaredError()(target_q_values, q_values)

    grads = tape.gradient(loss, q_network.trainable_variables)
    optimizer.apply_gradients(zip(grads, q_network.trainable_variables))


def train_ctde_dqn(env, num_agents, unit_action_space, player_action_space, num_episodes, max_steps, buffer_size, batch_size, epsilon=0.90, epsilon_decay=0.9999, epsilon_min=0.01):
    q_network = QNetwork(unit_action_space, player_action_space)
    target_q_network = QNetwork(unit_action_space, player_action_space)
    optimizer = Adam(learning_rate=0.001)

    replay_buffer = ReplayBuffer(buffer_size)

    # Ensure the models are built
    dummy_input = tf.convert_to_tensor([env.reset()], dtype=tf.float32)
    dummy_unit_sequences = tf.zeros((1, 1, unit_action_space), dtype=tf.float32)
    q_network(dummy_input, dummy_unit_sequences)
    target_q_network(dummy_input, dummy_unit_sequences)
    target_q_network.set_weights(q_network.get_weights())

    for episode in range(num_episodes):
        print(f"Episode {episode}")
        state = env.reset()
        for step in range(max_steps):
            actions = []
            state_tensor = tf.convert_to_tensor([state], dtype=tf.float32)
            for agent_id in range(num_agents):
                player_channel = state[:, :, 1]
                num_units = get_num_units(player_channel, agent_id)

                if num_units > 0:
                    if tf.random.uniform(()) < epsilon:
                        unit_actions = [UnitAction(tf.random.uniform((1,), minval=0, maxval=unit_action_space, dtype=tf.int32).numpy()[0]) for _ in range(num_units)]
                        player_action = PlayerAction(tf.random.uniform((1,), minval=0, maxval=player_action_space, dtype=tf.int32).numpy()[0])
                    else:
                        unit_sequences = tf.zeros((1, num_units, unit_action_space), dtype=tf.float32)
                        unit_q_values, player_q_values = q_network(state_tensor, unit_sequences=unit_sequences)
                        unit_actions = [UnitAction(action) for action in tf.argmax(unit_q_values[0, :num_units, :], axis=1).numpy().tolist()]
                        player_action = PlayerAction(tf.argmax(player_q_values[0, :]).numpy().tolist())

                else:
                    _, player_q_values = q_network(state_tensor, unit_sequences=tf.zeros((1, 1, unit_action_space), dtype=tf.float32))
                    player_action = PlayerAction(tf.argmax(player_q_values[0, :]).numpy().tolist())
                    unit_actions = []

                actions.append(unit_actions + [player_action])

            next_state, rewards, terminated, truncated, info = env.step(actions)

            if step == max_steps - 1:
                rewards = [reward - 100 for reward in rewards]

            print(f"Episode {episode} - Step {step} - Reward: {rewards} - Epsilon: {epsilon} - Terminated: {terminated}")

            replay_buffer.add((state, actions, rewards, next_state, terminated))
            state = next_state

            if replay_buffer.size() >= batch_size:
                for agent_id in range(num_agents):
                    experiences = replay_buffer.sample(batch_size)
                    train_agent(q_network, target_q_network, optimizer, experiences, agent_id)

            if (episode * max_steps + step) % 1000 == 0:
                print(f"Updating target network at episode {episode}")
                target_q_network.set_weights(q_network.get_weights())

            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

            if terminated:
                break


def create_unit_sequences(states, q_network, agent_id):
    unit_sequences = []
    max_units = 0

    for state in states:
        player_channel = state[:, :, 1]
        num_units = get_num_units(player_channel, agent_id)
        max_units = tf.maximum(max_units, num_units)
        unit_sequence = tf.zeros((num_units, q_network.unit_action_space), dtype=tf.float32)
        unit_sequences.append(unit_sequence)

    return pad_sequences(unit_sequences, max_units)


def pad_sequences(sequences, max_length):
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(
        sequences,
        maxlen=max_length,
        padding='post',
        dtype='float32'
    )
    return padded_sequences


def extract_agent_actions(actions, agent_id):
    """
    Extracts the actions corresponding to a specific agent from the list of actions.

    Parameters:
    actions (list): A list of actions taken by all agents.
    agent_id (int): The ID of the agent whose actions are to be extracted.

    Returns:
    list: A list of actions corresponding to the specified agent.
    """
    return [action[agent_id] for action in actions]


def get_unit_actions(agent_actions):
    """
    Converts the actions to their values and calculates the maximum number of unit actions.

    Parameters:
    agent_actions (list): A list of actions taken by a specific agent.

    Returns:
    tuple:
        - list: A list of lists containing the unit actions' values.
        - int: The maximum number of unit actions in any of the action lists.
    """
    unit_actions = []
    max_units = 0
    for action in agent_actions:
        unit_actions_list = [act.value for act in action[:-1]]
        max_units = max(max_units, len(unit_actions_list))
        unit_actions.append(unit_actions_list)
    return unit_actions, max_units


def pad_unit_actions(unit_actions, max_units):
    """
    Pads the unit actions to ensure they all have the same length.

    Parameters:
    unit_actions (list): A list of lists containing the unit actions' values.
    max_units (int): The maximum number of unit actions in any of the action lists.

    Returns:
    list: A list of lists containing the padded unit actions.
    """
    padded_unit_actions = []
    for actions_list in unit_actions:
        padding_length = max_units - len(actions_list)
        padded_actions = actions_list + [-1] * padding_length
        padded_unit_actions.append(padded_actions)
    return padded_unit_actions


# Initialize the environment and train the agents
grid_size = (10, 10)
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

game_engine.setup_agents()

num_agents = 2
unit_action_space = len(UnitAction)
player_action_space = len(PlayerAction)
num_episodes = 1000
max_steps = 100
buffer_size = 5000
batch_size = 32

env = GameEnv(game_engine, game_render, num_agents)

train_ctde_dqn(env, num_agents, unit_action_space, player_action_space, num_episodes, max_steps, buffer_size, batch_size)
