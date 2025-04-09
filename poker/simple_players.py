from player import Player
from actions import Action
import tkinter as tk
import asyncio
import random

class Command_Line_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)


    def make_move(self, game):
        #super().action(last_action)
        actions = {Action.FOLD: game.fold, Action.CHECK: game.check, Action.CALL: game.call, Action.RAISE: self.raise_bet, Action.BET:self.bet_method, Action.ALL_IN: game.all_in}
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


    def make_move(self, game):
        if game.ended == False:
            opposition_player = game.get_opponent_player(self)
            
            print(self.valid_actions)
            new_action = int(input("FOLD = 1, CHECK = 2, CALL = 3, BET = 4, RAISE = 5, ALL_IN = 6"))
            new_action = Action(new_action)
            print("ACTION:", new_action)
            amount = 0

            if new_action == Action.RAISE:
                amount = int(input(f"(Balance: {self.stack}) Raise/Bet Amount : "))
                if amount == self.stack:
                    game.all_in(self)
                game.raise_bet(self, amount)

            if new_action == Action.BET:
                amount = int(input(f"(Balance: {self.stack}) Raise/Bet Amount : "))
                if amount == self.stack:
                    game.all_in(self)
                game.bet(self, amount)
     
            elif new_action == Action.CALL:
                game.call(self)

            elif new_action == Action.ALL_IN:
                game.all_in(self)

            elif new_action == Action.FOLD:
                game.fold(self)

            elif new_action == Action.CHECK:
                game.check(self)

            print(f"{self}:", new_action, amount)
            return (new_action, amount)

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

        

    def update_available_actions(self, last_action):
        result = super().update_available_actions(last_action)
        print(result)
        return result

    

class Random_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
    
    def make_move(self, game):
        if game.ended == False:
            opposition_player = game.get_opponent_player(self)
            

            new_action = random.choice(self.valid_actions)
            print("ACTION:", new_action)
            amount = 0

            if new_action == Action.RAISE:
                amount = random.randint(min(self.stack, 2 * opposition_player.previous_bet) , self.stack)
                if amount == self.stack:
                    game.all_in(self)
                game.raise_bet(self, amount)

            if new_action == Action.BET:
                amount = random.randint(min(self.stack, 2 * opposition_player.previous_bet) , self.stack)
                if amount == self.stack:
                    game.all_in(self)
                game.bet(self, amount)
     
            elif new_action == Action.CALL:
                game.call(self)

            elif new_action == Action.ALL_IN:
                game.all_in(self)

            elif new_action == Action.FOLD:
                game.fold(self)

            elif new_action == Action.CHECK:
                game.check(self)

            print(f"{self}:", new_action, amount)
            return (new_action, amount)
