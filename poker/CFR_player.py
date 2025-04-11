from player import Player
from actions import Action
import torch
import torch.nn as nn
import torch.optim as optim
import random

class CFR_Player(Player):
    def __init__(self, player_id, name):
        super().__init__(player_id, name)
        # Define your PyTorch model
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),  # Replace with your input and hidden sizes
            nn.ReLU(),
            nn.Linear(hidden_size, output_size), # Replace with your output size (number of actions)
            nn.Softmax(dim=1)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.regret_sum = {} # Information set : regrets
        self.strategy_sum = {} # Information set : strategy sums

    def choose_action(self, available_actions, game_state):
        # Convert game_state to input for the model
        input_tensor = torch.tensor(self.encode_game_state(game_state), dtype=torch.float32).unsqueeze(0)
        action_probs = self.model(input_tensor)[0].detach().numpy()
        # Sample an action based on probabilities
        action = random.choices(available_actions, weights=action_probs)[0]
        # Update CFR regret values and strategy
        self.update_cfr(game_state, action)
        return action

    def encode_game_state(self, game_state):
        # Implement game state encoding
        # ...
        return encoded_state

    def update_cfr(self, game_state, action):
        # Implement CFR update logic
        # ...
        """"""
