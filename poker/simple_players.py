from player import Player
from actions import Action
import tkinter as tk
import asyncio
import random

class Command_Line_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)

    def action(self, last_action, call_amt):
        super().action(last_action)

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

    async def action(self, last_action):
        await self.get_action_from_user()
        print("GETTING ACTION:", action)

    async def async_action(choice):
        """
        Waits for a variable to change and returns its value using asyncio.
        """

        future = asyncio.Future()

        def set_future(value):
            future.set_result(value)

        def on_choice_change(*args):
            set_future(choice.get())
            root.quit()

        choice.trace("w", on_choice_change)
        root.mainloop()

        return await future

        

    def get_available_actions(self, last_action):
        result = super().get_available_actions(last_action)
        print(result)
        return result

    

class Random_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
    
    def action(self, last_action:tuple[Action, int], call_amt) -> list[Action]:
        possible_actions = self.get_available_actions(last_action)

        print(possible_actions)

        new_action = random.choice(possible_actions)
        amount = 0

        if new_action == Action.BET or new_action == Action.RAISE:
            amount = random.randint(min(self.stack, 2 * last_action[1]) , self.stack)
            if amount == self.stack:
                new_action = Action.ALL_IN
        elif new_action == Action.CALL:
            amount = call_amt

        if new_action == Action.ALL_IN:
            amount = self.stack

        print(new_action, amount)
        return (new_action, amount)
