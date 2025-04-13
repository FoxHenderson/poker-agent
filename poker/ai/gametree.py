import numpy as np
import random
from cmdlogic.actions import Action 
from cfr_player import AbstractActions

# represents the game state
class CFR_Node:
    def __init__(self, info_set):
        self.info_set:list[AbstractActions] = info_set

        self.regret_sum = [None] * AbstractActions.NUM_ACTIONS
        self.strategy = [None] * AbstractActions.NUM_ACTIONS
        self.strategy_sum = [None] * AbstractActions.NUM_ACTIONS

        self.NUM_LEGAL_ACTIONS = ...
    
    def getStrategy(self, realisation_weight:float) -> ...:
        """
        Get current information set mixed strategy through regret-matching
        """
        normalising_sum:float = 0

        for a in range(self.NUM_LEGAL_ACTIONS):
            if normalising_sum > 0:
                self.strategy[a] /= normalising_sum
            else:
                self.strategy[a] = 1 / self.NUM_LEGAL_ACTIONS
            strategy_sum += realisation_weight * self.strategy[a]
        return self.strategy
    
    def getAverageStrategy(self) -> list:
        """
        Get average information set mixed strategy across all training iterations
        """
        avg_strategy = [None] * self.NUM_LEGAL_ACTIONS
        normalising_sum = 0

        for a in range(self.NUM_LEGAL_ACTIONS):
            normalising_sum += self.strategy_sum[a]

        for a in range(self.NUM_LEGAL_ACTIONS):
            if normalising_sum > 0:
                avg_strategy[a] = self.strategy_sum[a] / normalising_sum
            else:
                avg_strategy[a] = 1 / self.NUM_LEGAL_ACTIONSs

        return avg_strategy