from game import Action

class Player:
    def __init__(self, ID:int, name:str):
        self.ID = ID
        self.name = name
        self.cards = []
        self.stack = 1000

        # pre-flop, flop, turn, river
        # actions of the form: f - fold, cx - call $x, rx - raise $x 
        self.action_history = [[], [], [], []]

    def show_hand(self):
        print (" ", self.cards[0].show_card(), "\n ", self.cards[1].show_card())
    
    def update_action(self, last_action:Enum, state):
        # preflop = 0, flop = 1, turn = 2, river = 3
        self.action_history[state].append(last_action)

    def get_last_action(self, state):
        if len(self.action_history[state]) > 0:
            return self.action_history[state][-1]
        return None