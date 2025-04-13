from enum import Enum
from .actions import Action


class Player:
    def __init__(self, ID:int, name:str):
        self.ID = ID
        self.name = name
        self.cards = []

        self.stack = 1000
        self.bet = 0 # amount bet in the current round


        self.folded = False
        self.all_in = False


        self.valid_actions = []

        # pre-flop, flop, turn, river
        # actions of the form: (Action, amount) e.g (Raise, 50) or (Check, 0)
        self.action_history = [[], [], [], []]

    def __str__(self):
        return (f"{self.name}: {self.stack}")

      
    def show_hand(self) -> str:
        print (f"{self.cards[0].show_card()}, {self.cards[1].show_card()}")


    def get_available_actions(self, last_action:tuple[Action, int]) -> list:
        last_act = last_action[0]
        last_amt = last_action[1]


        self.valid_actions = [Action.FOLD]
        if last_act is None:
            return [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]

        match last_act:
            case Action.FOLD:
                # case shouldn't be achieved
                self.valid_actions = []
                return self.valid_actions
            case Action.CHECK:
                self.valid_actions =  [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]
                return self.valid_actions
            case Action.CALL:
                self.valid_actions = [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]
                return self.valid_actions
            case Action.BET:
                self.valid_actions.append(Action.ALL_IN)
                if self.stack > last_amt:
                    self.valid_actions.append(Action.CALL)
                    self.valid_actions.append(Action.RAISE)
            case Action.RAISE:
                self.valid_actions.append(Action.ALL_IN)
                if self.stack > last_amt:
                    self.valid_actions.append(Action.CALL)
                    self.valid_actions.append(Action.RAISE)
            case Action.ALL_IN:
                self.valid_actions.append(Action.CALL)
        return self.valid_actions