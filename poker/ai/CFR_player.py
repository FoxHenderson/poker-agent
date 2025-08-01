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



    def update_available_actions(self, last_action:tuple[Action, int]) -> list:
        self.valid_actions = self.get_available_actions(last_action)
        return self.valid_actions

    #"""I AM GONNA CHANGE THE BELOW CODE!"""#

    def get_available_actions(self, last_action:tuple[Action, int]) -> list:

        if last_action is None:
            valid_actions = [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, AbstractAction.ALL_IN]
            return valid_actions
        last_act = last_action[0]
        last_amt = last_action[1]


        valid_actions = [AbstractAction.FOLD]
        

        match last_act:
            case Action.FOLD:
                # case shouldn't be achieved
                valid_actions = []
                return valid_actions
            case Action.CHECK:
                valid_actions =  [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, Action.ALL_IN]
                return valid_actions
            case Action.CALL:
                # case shouldn't be achieved.
                valid_actions = [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, AbstractAction.ALL_IN]
                return valid_actions
            case Action.BET:
                valid_actions.append(AbstractAction.ALL_IN)
                if self.stack > last_amt:
                    valid_actions.append(AbstractAction.CALL)
                    valid_actions.append(AbstractAction.RAISE_HALF)
                    valid_actions.append(AbstractAction.RAISE_POT)
            case Action.RAISE:
                self.valid_actions.append(Action.ALL_IN)
                if self.stack > last_amt:
                    valid_actions.append(AbstractAction.CALL)
                    valid_actions.append(AbstractAction.RAISE_HALF)
                    valid_actions.append(AbstractAction.RAISE_POT)
                print(self.valid_actions)
            case Action.ALL_IN:
                valid_actions.append(AbstractAction.CALL)
            
        return valid_actions



    def make_move(self, game, action):
            opposition_player = game.get_opponent_player(self)
            

            new_action = action
            print("ACTION:", new_action)
            amount = 0
           

                
            if new_action == AbstractAction.RAISE_HALF:
                amount = game.pot // 2
                if amount >= self.stack:
                    game.all_in(self)
                if game.raise_bet(self, amount) == False:
                    return False

            if new_action == AbstractAction.RAISE_POT:
                amount = game.pot
                if amount >= self.stack:
                    game.all_in(self)
                if game.raise_bet(self, amount) == False:
                    return False

            if new_action == AbstractAction.BET_HALF:
                amount = game.pot //2
                if amount >= self.stack:
                    game.all_in(self)
                if game.bet(self, amount) == False:
                    return False

            if new_action == AbstractAction.BET_POT:
                amount = game.pot
                if amount >= self.stack:
                    game.all_in(self)
                if game.bet(self, amount) == False:
                    return False
     
            elif new_action == AbstractAction.CALL:
                game.call(self)

            elif new_action == AbstractAction.ALL_IN:
                game.all_in(self)

            elif new_action == AbstractAction.FOLD:
                game.fold(self)

            elif new_action == AbstractAction.CHECK:
                game.check(self)

            print(f"{self}:", new_action, amount)
            return (new_action, amount)



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
"""
    def update_available_actions(self, last_action:tuple[Action, int]) -> list:
        #print("LAST ACTION:", last_action)
        if last_action is None:
            return [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, AbstractAction.ALL_IN]

        
        last_act = last_action[0]
        last_amt = last_action[1]


        self.valid_actions = [AbstractAction.FOLD]
        if last_act is None:
            return [Action.FOLD, Action.CHECK, Action.BET, Action.ALL_IN]

        match last_act:
            case Action.FOLD:
                # case shouldn't be achieved
                self.valid_actions = []
                return self.valid_actions
            case Action.CHECK:
                self.valid_actions =  [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, AbstractAction.ALL_IN]
                return self.valid_actions
            case Action.CALL:
                # case shouldn't be achieved.
                self.valid_actions = [AbstractAction.FOLD, AbstractAction.CHECK, AbstractAction.BET_HALF, AbstractAction.BET_POT, AbstractAction.ALL_IN]
                return self.valid_actions
            case Action.BET:
                self.valid_actions.append(AbstractAction.ALL_IN)
                if self.stack > last_amt:
                    self.valid_actions.append(AbstractAction.CALL)
                    self.valid_actions.append(AbstractAction.BET_HALF)
                    self.valid_actions.append(AbstractAction.BET_POT)
            case Action.RAISE:
                self.valid_actions.append(AbstractAction.ALL_IN)
                if self.stack > last_amt:
                    self.valid_actions.append(AbstractAction.CALL)
                    self.valid_actions.append(AbstractAction.BET_HALF)
                    self.valid_actions.append(AbstractAction.BET_POT)
            case Action.ALL_IN:
                self.valid_actions.append(AbstractAction.CALL)
            
        return self.valid_actions
"""
    
    
   # def get_available_actions(self, last_action:tuple[Action, int]) -> list:
    #    return self.update_available_actions(last_action)


