from player import Player
from game import Action
import random

class Random_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
    
    def get_action(self, last_action:Action, amount:int):
        possible_actions = last_action.get_actions()





        new_action = random.choice(possible_actions)

        if new_action == Action.Check or new_action == Action.Fold or call:
        elif new_action == Action.Raise:
            
            
        return (new_action, 0)

        