#from gametree import CFR_Node
from cmdlogic.player import Player
from cmdlogic.card import Card
from cmdlogic.actions import Action
from cmdlogic.abstracted_actions import AbstractAction

class CFR_Player(Player):
    def __init__(self, ID:int, name:str):
        super().__init__(ID, name)
        self.info_sets = {}

    def action(self, last_action, call_amt):
        valid_actions = self.get_available_actions(last_action)

        chosen_action = ... # somehow get the action 

    # THIS IS USED FOR TRAINING SO IT WILL USE THE ABSTRACTED ACTIONS ONLY FOR NOW - FOX
    # BECAUSE OF THE NATURE OF THE TRAINING, BOTH PLAYERS WILL HAVE THEIR STACKS RESET AFTER EACH HAND
    # THIS MEANS THAT THERE ARE NO ALL IN DISCREPENCIES!
    

    #"""I AM GONNA CHANGE THE BELOW CODE!"""#

    """
    def get_available_actions(self, last_action:AbstractActions):
        if last_action == AbstractActions.CHECK_FOLD:
            return [
                AbstractActions.CHECK_FOLD,
                AbstractActions.CALL, 
                AbstractActions.BET_HALF,
                AbstractActions.BET_POT,
                AbstractActions.ALL_IN
            ]
        elif last_action == AbstractActions.CHECK_FOLD:
            return [
                AbstractActions.CHECK_FOLD,
                AbstractActions.CALL, 
                AbstractActions.BET_HALF,
                AbstractActions.BET_POT,
                AbstractActions.ALL_IN
            ]
        else:
            return [
                AbstractActions.CHECK_FOLD,
                AbstractActions.BET_HALF,
                AbstractActions.BET_POT,
                AbstractActions.ALL_IN
            ]
    """

    def update_available_actions(self, last_action:tuple[Action, int]) -> list:
        if last_action is None:
            return [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]

        
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

    def get_available_actions(self, last_action:tuple[Action, int]) -> list:
        return self.update_available_actions(last_action)
