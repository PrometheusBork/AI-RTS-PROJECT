import numpy as np
from collections import deque, namedtuple

Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'terminate'])


class PrioritizedReplayBuffer:
    def __init__(self, buffer_size, alpha=0.6, beta=0.4, beta_increment_per_sample=0.001):
        self.buffer = deque(maxlen=buffer_size)
        self.priorities = deque(maxlen=buffer_size)
        self.alpha = alpha
        self.beta = beta
        self.beta_increment_per_sample = beta_increment_per_sample

    def add(self, experience):
        max_priority = max(self.priorities) if self.buffer else 1.0
        self.buffer.append(experience)
        self.priorities.append(max_priority)

    def sample(self, batch_size):
        priorities = np.array(self.priorities)
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()
        indices = np.random.choice(len(self.buffer), batch_size, p=probabilities, replace=False)
        experiences = [self.buffer[idx] for idx in indices]

        total_priority = np.sum(priorities[indices])
        weights = (total_priority ** self.beta) * (1 / probabilities[indices]) ** (1 - self.beta)
        weights /= weights.max()

        self.beta = min(1.0, self.beta + self.beta_increment_per_sample)

        return experiences, indices, weights

    def update_priorities(self, indices, new_priorities):
        for idx, priority in zip(indices, new_priorities):
            self.priorities[idx] = priority ** self.alpha

    def size(self):
        return len(self.buffer)