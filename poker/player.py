from enum import Enum
from actions import Action



class Player:
    def __init__(self, ID:int, name:str):
        self.ID = ID
        self.name = name
        self.cards = []

        self.stack = 1000
        self.bet = 0 # amount bet in the current round
        self.previous_bet = 0
        self.betting_history = []

        self.valid_actions = []

        self.folded = False
        self.all_in = False

        # pre-flop, flop, turn, river
        # actions of the form: (Action, amount) e.g (Raise, 50) or (Check, 0)
        self.action_history = [[], [], [], []]

    def __str__(self):
        return (f"{self.name}: {self.stack}")

    
    def add_bet(self, bet_amount):
        self.previous_bet = bet_amount
        self.betting_history.append(self.previous_bet)

        
    def show_hand(self) -> str:
        print (f"{self.cards[0].show_card()}, {self.cards[1].show_card()}")
    
    def update_action(self, game_state, last_action:Action, amount=0):
        # preflop = 0, flop = 1, turn = 2, river = 3
        self.action_history[game_state].append(last_action)

    def get_last_action(self, state):
        if len(self.action_history[state]) > 0:
            return self.action_history[state][-1]
        return None

    def action(self, last_action:tuple[Action, int], call_amt):
        valid_actions = self.get_available_actions(last_action)
        ...

    def update_available_actions(self, last_action:tuple[Action, int]) -> list:
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
                # case shouldn't be achieved.
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



