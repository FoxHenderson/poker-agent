from player import Player
from game import Action
import random

class Command_Line_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)

    def action(self, last_action, amount):
        super().action(last_action, amount)

    def get_available_actions(self, last_action, amount):
        result = super().get_available_actions(last_action, amount)
        print(result)
        return result


class Random_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
    
    def action(self, last_action:Action, min_amount:int):
        possible_actions = self.get_available_actions(last_action, min_amount)

        new_action = random.choice(possible_actions)
        amount = 0

        if new_action == Action.BET or new_action == Action.RAISE:
            amount = random.randint(min(self.stack, min_amount) , self.stack)
            if amount == amount:
                new_action = Action.ALL_IN

        return (new_action, amount)