import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import numpy as np
import random
from constants import *
from collections import deque

class AI(object):
    """docstring for AI."""




    def __init__(self, input_shape, num_actions):
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.model = self.create_model()

        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32
        self.memory = deque(maxlen=2000)
        self.total_reward = 0


    def create_model(self):
        self.model = Sequential([
            Input(shape=(self.input_shape,)),  # Define the input shape explicitly
            Dense(128, activation='relu'),
            Dense(128, activation='relu'),
            Dense(self.num_actions, activation='linear')  # Output Q-values for each action
        ])
        self.model.compile(optimizer='adam', loss='mse')
        return self.model



    def choose_action(self, state):
        state = np.array([state])  # Make sure state is in the right shape
        q_values = self.model.predict(state)

        # Debug output
        print(f"Q-values: {q_values}, Shape: {q_values.shape}")

        # Check for unexpected results
        if q_values is None or np.any(np.isnan(q_values)):
            print("Warning: Q-values are None or NaN.")
            return random.randrange(self.num_actions)  # Fallback to random action

        return np.argmax(q_values[0])  # Exploit



    def get_state(self, snake, apple):
        # Normalize positions relative to grid
        state = [
            snake.x / GAME_WIDTH, snake.y / GAME_HEIGHT,  # Snake head position
            apple.x / GAME_WIDTH, apple.y / GAME_HEIGHT  # Apple position
        ]
        print(f"state:{state}")
        # Add body positions as flattened list
        for segment in snake.body:
            state.extend([segment[0] / GAME_WIDTH, segment[1] / GAME_HEIGHT])

        while len(state) < 20:
            state.append(0.0)
        return state[:20]


    def train(self, snake, apple):
        # self.total_reward = 0
        state = self.get_state(snake, apple)
        action = self.choose_action(state)

        # Simulate the snake's action and update the state
        snake.key_handler(action)
        snake.update(apple)

        # Get new state, reward, and done flag
        new_state = self.get_state(snake, apple)
        reward = 1 if snake.x == apple.x and snake.y == apple.y else -0.1  # Reward for eating apple
        done = snake.bounds_check() or snake.check_body_collide()

        # Store experience in memory
        self.memory.append((state, action, reward, new_state, done))
        state = new_state
        self.total_reward += reward

        # Print score when the episode ends
        if done:
            print(f"Score: {snake.score}, Reward: {self.total_reward}")
            snake.reset()
            apple.new_loc()  # Reset apple position when the game ends

        # Train the model with a batch of experiences
        if len(self.memory) > self.batch_size:
            minibatch = random.sample(self.memory, self.batch_size)
            for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    target += self.gamma * np.max(self.model.predict(np.array([next_state]))[0])

                # Predict Q-values and update them for the chosen action
                q_values = self.model.predict(np.array([state]))
                q_values[0][action] = target

                # Train the model
                self.model.fit(np.array([state]), q_values, verbose=0)

        # Decay epsilon for exploration-exploitation balance
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    # def train(self, snake, apple):
        # self.total_reward = 0
        # state = self.get_state(snake, apple)
        # action = self.choose_action(state)
        # snake.key_handler(action)
        # snake.update(apple)
        #
        # # Get new state, reward, and done
        # new_state = self.get_state(snake, apple)
        # reward = 1 if snake.x == apple.x and snake.y == apple.y else -0.1  # Customize reward
        # done = (snake.bounds_check() or snake.check_body_collide())
        #
        # # Store in memory
        # self.memory.append((state, action, reward, new_state, done))
        # state = new_state
        # self.total_reward += reward
        #
        # if done:
        #     print(f" Score: {snake.score}, Reward: {self.total_reward}")
        #     snake.reset()
        #
        # # Train the model
        # if len(self.memory) > self.batch_size:
        #     minibatch = random.sample(self.memory, self.batch_size)
        #     for state, action, reward, next_state, done in minibatch:
        #         target = reward
        #         if not done:
        #             target += self.gamma * np.max(self.model.predict(np.array([next_state]))[0])
        #         q_values = self.model.predict(np.array([state]))
        #         q_values[0][action] = target
        #         self.model.fit(np.array([state]), q_values, verbose=0)
        #
        # # Decrease epsilon
        # if self.epsilon > self.epsilon_min:
        #     self.epsilon *= self.epsilon_decay
