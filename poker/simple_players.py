from player import Player
from actions import Action
import tkinter as tk
import asyncio
import random

class Command_Line_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)


    def madfghke_move(self, game):
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
    

    def choose_move():
        return random.choice(self.valid_actions)

    
    def make_move(self, game):
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


# GAME STATS
"""
PLAYERS CARDS
COMMUNITY CARDS
POT SIZE
BETTING HISTORY~
PLAYERS CHIP STACK
OPPONENTS CHIP STACK

"""




class Simple_CFR_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
        


    def get_player_game_stats(self, game):
        opponent = game.get_opponent_player(self)

        # WE WANT TO FEED IN A SET OF STATS AS VECTOR PARAMETERS INTO THE NEURAL NETWORK, THEREFORE, THEY ALL NEED TO BE NUMERICAL VALUES:
        
        player_cards = self.cards #Run your evaluation function on this to make it numerical
        community_cards = game.board #Same here - How does the function handle None - are you able to simply remove these before evaluation!?
        pot_size = game.pot # This is already a numerical value - YIPPEEEE


        """self_action_history = self.action_history""" # Need to numerically define the strength of an action. - For example, raising a bet may suggest a higher confidence in the opponents hand compared to simply calling! 
        """opponent_action_history = opponent.action_history""" #similar here - although be aware that bluffing is a perfectly valid poker tactic which may be being used

        self_bet_history = self.betting_history
        opponent_bet_history = opponent.betting_history

        self_chip_stack = self.stack # Already a numerical value - HAPPY TIMES
        opponent_chip_stack = opponent.stack # HAPPY TIMES continued here!

        return [player_cards, community_cards, pot_size, self_bet_history, opponent_bet_history, self_chip_stack, opponent_chip_stack]
        

    

    def choose_move(self):
        return random.choice(self.valid_actions)

    
    def make_move(self, game):
            opposition_player = game.get_opponent_player(self)
            

            new_action = self.choose_move()
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
