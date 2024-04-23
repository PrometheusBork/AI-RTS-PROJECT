import random
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam


class DQL:
    def __init__(self, player, state_size, action_size):
        self.player = player
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self.create_model()  # Not in use currently

    def act(self, state):
        return random.randint(1, 6), self.player

    # For experience replay, not in use currently
    def remember(self, state, action, reward, next_state, done):
        pass

    # Deprecated
    def train(self, game_env, num_episodes, batch_size):
        for episode in range(num_episodes):
            state = game_env.reset() if episode != 0 else None
            # state = np.reshape(state, [1, self.state_size])
            terminated = False
            while not terminated:
                action = self.act(state)
                next_state, reward, terminated, truncated, info = game_env.step(action)
                state = next_state
            print(f'Episode: {episode}/{num_episodes}')

    def save(self, path):
        pass

    def load(self, path):
        pass

    def create_model(self):
        model = Sequential()
        # model.add(Flatten(input_shape=(1 + self.state_size)))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
