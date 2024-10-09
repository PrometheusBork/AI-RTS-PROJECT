import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, GRU, Embedding, LayerNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Model
import datetime

from src.game.constants.PlayerAction import PlayerAction
from src.game.constants.UnitAction import UnitAction
from src.ai.utils import get_num_units, extract_agent_actions, get_unit_actions, pad_unit_actions, create_unit_sequences
from src.ai.PrioritizedReplayBuffer import PrioritizedReplayBuffer
from src.game.engines.GameEngine import GameEngine
from src.game.engines.RenderEngine import RenderEngine
from src.game.managers.StateManager import GameStateManager
from src.game.maps.Map import Map
from src.ai.envs.GameEnv import GameEnv


@tf.keras.utils.register_keras_serializable()
class QNetwork(Model):
    def __init__(self, unit_action_space, player_action_space):
        super(QNetwork, self).__init__()
        self.initial_state = tf.zeros((1, 64))
        self.unit_action_space = unit_action_space
        self.player_action_space = player_action_space

        self.conv1 = Conv2D(32, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')
        self.conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')
        self.conv3 = Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')
        self.pool = MaxPooling2D((2, 2))
        self.flatten = Flatten()
        self.dense1 = Dense(128, activation='relu', kernel_initializer='he_normal')
        self.dense2 = Dense(64, activation='relu', kernel_initializer='he_normal')

        self.unit_rnn = GRU(64, return_sequences=True, return_state=True, kernel_initializer='he_normal')
        self.unit_dense = Dense(unit_action_space, activation='linear', kernel_initializer='he_normal')
        self.player_dense = Dense(player_action_space, activation='linear', kernel_initializer='he_normal')

    def call(self, inputs, unit_sequences):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.pool(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)

        # Reshape x to be compatible with GRU input
        x_reshaped = tf.expand_dims(x, axis=1)
        x_reshaped = tf.tile(x_reshaped, [1, tf.shape(unit_sequences)[1], 1])

        # Process the reshaped convolutional output with the GRU layer
        unit_q_values, _ = self.unit_rnn(x_reshaped, initial_state=self.initial_state)
        unit_q_values = self.unit_dense(unit_q_values)

        player_q_values = self.player_dense(x)

        return unit_q_values, player_q_values

    def get_config(self):
        config = super(QNetwork, self).get_config()
        config.update({
            'unit_action_space': self.unit_action_space,
            'player_action_space': self.player_action_space
            #'num_agents': self.num_agents
        })
        return config

    @classmethod
    def from_config(cls, config):
        return cls(
            unit_action_space=config['unit_action_space'],
            player_action_space=config['player_action_space']
            #num_agents=config['num_agents'],
            **config
        )

    def build_from_config(self, config):
        self.build((None, 10, 10, 2))


def train_agent(q_network, target_q_network, optimizer, replay_buffer, agent_id, batch_size):
    experiences, indices, weights = replay_buffer.sample(batch_size)
    states, actions, rewards, next_states, terminates = zip(*experiences)

    states = tf.convert_to_tensor(states, dtype=tf.float32)
    next_states = tf.convert_to_tensor(next_states, dtype=tf.float32)
    rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)
    terminates = tf.convert_to_tensor(terminates, dtype=tf.float32)
    weights = tf.convert_to_tensor(weights, dtype=tf.float32)

    batch_size = states.shape[0]
    rewards = tf.reshape(rewards[:, agent_id], [batch_size])

    unit_sequences = create_unit_sequences(states, q_network.unit_action_space, agent_id)
    next_unit_sequences = create_unit_sequences(next_states, q_network.unit_action_space, agent_id)

    next_unit_q_values, next_player_q_values = target_q_network(next_states, unit_sequences=next_unit_sequences)
    max_next_unit_q_values = tf.reduce_max(next_unit_q_values, axis=1)
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

        # Compute the importance-weighted TD errors
        td_errors = tf.abs(target_q_values - q_values)
        loss = tf.reduce_mean(weights * td_errors)

    grads = tape.gradient(loss, q_network.trainable_variables)
    optimizer.apply_gradients(zip(grads, q_network.trainable_variables))

    # Update the priorities in the replay buffer
    new_priorities = td_errors.numpy() + 1e-6  # Add a small positive value to avoid zero priorities
    replay_buffer.update_priorities(indices, new_priorities)

    return loss


def train_ctde_dqn(env, num_agents, unit_action_space, player_action_space, num_episodes, max_steps, buffer_size, batch_size, epsilon=1.0, epsilon_decay=0.9999, epsilon_min=0.01):
    q_network = QNetwork(unit_action_space, player_action_space)
    target_q_network = QNetwork(unit_action_space, player_action_space)
    target_q_network.set_weights(q_network.get_weights())
    optimizer = Adam(learning_rate=0.001)

    replay_buffer = PrioritizedReplayBuffer(buffer_size)

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    summary_writer = tf.summary.create_file_writer(log_dir)
    summary_writer.set_as_default()

    # Build the models
    dummy_state = tf.convert_to_tensor([env.reset()], dtype=tf.float32)
    dummy_unit_sequences = tf.zeros((1, 1, unit_action_space), dtype=tf.float32)
    q_network(dummy_state, dummy_unit_sequences)
    target_q_network(dummy_state, dummy_unit_sequences)

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    summary_writer = tf.summary.create_file_writer(log_dir)
    summary_writer.set_as_default()

    for episode in range(num_episodes):
        state = env.reset()
        episode_rewards = [0.0 for _ in range(num_agents)]
        episode_losses = []
        terminated = False

        for step in range(max_steps):
            actions = []
            state_tensor = tf.convert_to_tensor([state], dtype=tf.float32)

            for agent_id in range(num_agents):
                player_channel = state[:, :, 1]
                num_units = get_num_units(player_channel, agent_id)

                if tf.random.uniform(()) < epsilon:
                    # Random actions
                    unit_actions = [UnitAction(tf.random.uniform((1,), minval=0, maxval=unit_action_space, dtype=tf.int32)) for _ in range(num_units)]
                    player_action = PlayerAction(tf.random.uniform((1,), minval=0, maxval=player_action_space, dtype=tf.int32))
                else:
                    # Greedy actions based on Q-values
                    unit_sequences = tf.zeros((1, max(num_units, 1), unit_action_space), dtype=tf.float32)
                    unit_q_values, player_q_values = q_network(state_tensor, unit_sequences=unit_sequences)

                    if num_units > 0:
                        unit_actions = [UnitAction(action) for action in tf.argmax(unit_q_values[0, :num_units, :], axis=1).numpy()]
                    else:
                        unit_actions = []

                    player_action = PlayerAction(tf.argmax(player_q_values[0, :]).numpy())

                actions.append(unit_actions + [player_action])

            next_state, rewards, terminated, truncated, info = env.step(actions)

            if step == max_steps - 1:
                rewards = [reward - 100 for reward in rewards]

            replay_buffer.add((state, actions, rewards, next_state, terminated))
            state = next_state

            for agent_id in range(num_agents):
                episode_rewards[agent_id] += rewards[agent_id]

            if replay_buffer.size() >= batch_size:
                for agent_id in range(num_agents):
                    loss = train_agent(q_network, target_q_network, optimizer, replay_buffer, agent_id, batch_size)
                    episode_losses.append(loss)

            if (episode * max_steps + step) % 1000 == 0:
                print(f"Updating target network at episode {episode}")
                target_q_network.set_weights(q_network.get_weights())
                print("Saving models")
                q_network.save("q_network_v_old.keras")
                target_q_network.save("target_q_network_v_old.keras")

            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

            if terminated:
                break

        with summary_writer.as_default():
            player_stats = env.get_player_stats()
            for agent_id in range(num_agents):
                tf.summary.scalar(f'Agent {agent_id} Episode Reward', float(episode_rewards[agent_id]), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Units Created', float(player_stats[agent_id]['units_created']), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Units Destroyed', float(player_stats[agent_id]['units_destroyed']), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Units Lost', float(player_stats[agent_id]['units_lost']), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Resources Collected', float(player_stats[agent_id]['resources_collected']), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Bases Destroyed', float(player_stats[agent_id]['bases_destroyed']), step=episode)
                tf.summary.scalar(f'Agent {agent_id} Has Lost', float(player_stats[agent_id]['has_lost']), step=episode)
            tf.summary.scalar('Total Episode Reward', float(sum(episode_rewards)), step=episode)
            tf.summary.scalar('Average Loss', tf.reduce_mean(episode_losses), step=episode)
            tf.summary.scalar('Epsilon', epsilon, step=episode)
            tf.summary.scalar('Terminated', float(terminated), step=episode)

    summary_writer.close()


# Initialize the environment and train the agents
grid_size = (10, 10)
tile_size = 50
screen_size = (grid_size[0] * tile_size + (2 * tile_size), grid_size[1] * tile_size + (2 * tile_size))

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
max_steps = 300
buffer_size = 10000
batch_size = 64

env = GameEnv(game_engine, game_render, num_agents)

train_ctde_dqn(env, num_agents, unit_action_space, player_action_space, num_episodes, max_steps, buffer_size, batch_size)
