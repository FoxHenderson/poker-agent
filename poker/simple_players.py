from player import Player
from actions import Action
import tkinter as tk
import asyncio
import random

class Command_Line_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)

    def action(self, last_action, call_amt):
        #super().action(last_action)

        my_action = int(input("FOLD = 1, CHECK = 2, CALL = 3, BET = 4, RAISE = 5, ALL_IN = 6"))
        my_action = Action(my_action)

        amt = 0

        if my_action == Action.RAISE or my_action == Action.BET:
            amt = int(input(f"(Balance: {self.stack}) Raise/Bet Amount : "))
            if amt == self.stack:
                my_action = Action.ALL_IN
        elif my_action == Action.CALL:
            amt = call_amt

        if my_action == Action.ALL_IN:
            amt = self.stack

        return (my_action, amt)

    def get_available_actions(self, last_action):
        result = super().get_available_actions(last_action)
        print(result)
        return result



class Person_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
        self.current_action = None

    def make_move(self, last_action):
        print("WAITING FOR USER TO MAKE A MOVE", action)

        

    def get_available_actions(self, last_action):
        result = super().get_available_actions(last_action)
        print(result)
        return result

    

class Random_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
    
    def make_move(self, game):

        opposition_player = game.get_opponent_player(self)
        last_action = opposition_player.action_history[-1]
        possible_actions = self.get_available_actions(last_action)

        new_action = random.choice(possible_actions)
        amount = 0

        if new_action == Action.RAISE:
            amount = random.randint(min(self.stack, 2 * last_action[1]) , self.stack)
            if amount == self.stack:
                game.all_in(self)
            game.raise_bet(self, amount)

        if new_action == Action.BET:
            amount = random.randint(min(self.stack, 2 * last_action[1]) , self.stack)
            if amount == self.stack:
                game.all_in(self)
            game.bet(self, amount)
 
        elif new_action == Action.CALL:
            game.call(self)

        elif new_action == Action.ALL_IN:
            game.all_in(self)

        print("computer:", new_action, amount)
        return (new_action, amount)
