# q_learning.py

import numpy as np
import random
import pickle
import os

class QLearningAgent:
    def __init__(self, game, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1, q_table_file='q_table.pkl'):
        self.game = game
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table_file = q_table_file
        self.q_table = self.load_q_table()

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_q_table(self):
        with open(self.q_table_file, 'wb') as f:
            pickle.dump(self.q_table, f)

    def clear_q_table(self):
        self.q_table = {}
        if os.path.exists(self.q_table_file):
            os.remove(self.q_table_file)

    def get_state(self):
        return tuple(self.game.board)

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def set_q_value(self, state, action, value):
        self.q_table[(state, action)] = value

    def choose_action(self, valid_moves):
        if not valid_moves:
            return None

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_moves)
        else:
            state = self.get_state()
            q_values = [self.get_q_value(state, move) for move in valid_moves]
            max_q_value = max(q_values)
            max_q_actions = [valid_moves[i] for i in range(len(valid_moves)) if q_values[i] == max_q_value]
            return random.choice(max_q_actions)

    def update_q_value(self, state, action, reward, next_state, next_valid_moves):
        current_q = self.get_q_value(state, action)
        max_future_q = max([self.get_q_value(next_state, move) for move in next_valid_moves], default=0)
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_future_q)
        self.set_q_value(state, action, new_q)

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
