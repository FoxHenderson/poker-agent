from gametree import CFR_Node
from cmdlogic.player import Player
from cmdlogic.card import Card

# abstracted actions
class AbstractActions:
    CHECK_FOLD = 0,
    CALL = 1
    BET_HALF = 2 # bet half pot
    BET_POT = 3
    ALL_IN = 4

    NUM_ACTIONS = 5

class CFR_Player(Player):


    def action(self, last_action, call_amt):
        valid_actions = self.get_available_actions(last_action)

        chosen_action = ... # somehow get the action 

    # THIS IS USED FOR TRAINING SO IT WILL USE THE ABSTRACTED ACTIONS ONLY FOR NOW - FOX
    # BECAUSE OF THE NATURE OF THE TRAINING, BOTH PLAYERS WILL HAVE THEIR STACKS RESET AFTER EACH HAND
    # THIS MEANS THAT THERE ARE NO ALL IN DISCREPENCIES!
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