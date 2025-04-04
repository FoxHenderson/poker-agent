from enum import Enum
from actions import Action



class Player:
    def __init__(self, ID:int, name:str):
        self.ID = ID
        self.name = name
        self.cards = []

        self.stack = 1000
        self.bet = 0 # amount bet in the current round

        self.folded = False
        self.all_in = False

        # pre-flop, flop, turn, river
        # actions of the form: (Action, amount) e.g (Raise, 50) or (Check, 0)
        self.action_history = [[], [], [], []]

    def __repr__(self):
        print(f"{self.name}: {self.stack}")

    def show_hand(self) -> str:
        print (" ", self.cards[0].show_card(), "\n ", self.cards[1].show_card())
    
    def update_action(self, game_state, last_action:Action, amount=0):
        # preflop = 0, flop = 1, turn = 2, river = 3
        self.action_history[game_state].append(last_action)

    def get_last_action(self, state):
        if len(self.action_history[state]) > 0:
            return self.action_history[state][-1]
        return None

    def action(self, last_action:tuple[Action, int]):
        valid_actions = self.get_available_actions(last_action)
        ...

    def get_available_actions(self, last_action:tuple[Action, int]) -> list:
        last_act = last_action[0]
        last_amt = last_action[1]

        if last_act is None:
            return [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]

        possible_actions = [Action.FOLD]
        match last_act:
            case Action.FOLD:
                # case shouldn't be achieved 
                raise Exception("Get actions from FOLD")
            case Action.CHECK:
                return [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]
            case Action.CALL:
                # case shouldn't be achieved.
                raise Exception("Get actions from CALL")
            case Action.BET:
                possible_actions.append(Action.ALL_IN)
                if self.stack > last_amt:
                    possible_actions.append(Action.CALL)
                    possible_actions.append(Action.RAISE)
            case Action.RAISE:
                possible_actions.append(Action.ALL_IN)
                if self.stack > last_amt:
                    possible_actions.append(Action.CALL)
                    possible_actions.append(Action.RAISE)
            case Action.ALL_IN:
                possible_actions.append(Action.CALL)
            
        return possible_actions