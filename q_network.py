import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def create_model(input_shape, num_actions):
    model = Sequential([
        Dense(128, input_shape=(input_shape,), activation='relu'),
        Dense(128, activation='relu'),
        Dense(num_actions, activation='linear')  # Q-values for each action
    ])
    model.compile(optimizer='adam', loss='mse')
    return model
