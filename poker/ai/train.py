from cmdlogic.game import Game
from cmdlogic.card import Card
from cmdlogic.abstracted_actions import AbstractAction
from CFR_player import CFR_Player

from copy import deepcopy
from CFRState import CFR_State



# implementation baed on  http://modelai.gettysburg.edu/2013/cfr/cfr.pdf

class CFR_Trainer:
    def __init__(self, iterations:int=10):
        self.iterations = iterations
        
        self.info_sets = {} # maps str -> InformationSet

        self.train()




    def cfr_recursive(self, game: Game, state: CFR_State):

        
        if state.is_terminal():
            return game.get_terminal_values()
        
        player_to_act = game.players[game.to_act_index]
        possible_actions = state.get_possible_actions()


        for action in possible_actions:
            next_game = deepcopy(game)
            next_state = CFR_State(next_game, state.player_id)

            print(f"Exploring action: {action} from player {player_to_act.name} in round {next_game.round_index}")
            if action == AbstractAction.FOLD and AbstractAction.CHECK in possible_actions:
                action = AbstractAction.CHECK


            if action == AbstractAction.FOLD:
                next_game.fold(player_to_act)

            if action == AbstractAction.CHECK:
                next_game.check(player_to_act)

            if action == AbstractAction.CALL:
                next_game.call(player_to_act)

            if action == AbstractAction.BET_HALF:
                next_game.bet(player_to_act, (state.get_pot()/2))

            if action == AbstractAction.BET_POT:
                next_game.bet(player_to_act, state.get_pot())

            if action == AbstractAction.ALL_IN:
                next_game.all_in(player_to_act)

            next_player_id = (state.player_id + 1) % len(next_game.players)
            next_state = CFR_State(next_game, next_player_id)
            action_values[action] = self.cfr_recursive(next_game, next_state)
            

        
    def train(self):
        player1 = CFR_Player(1, "Player1")
        player2 = CFR_Player(2, "Player2")
        

        for iteration in range(self.iterations):
            game = Game(player1, player2)
            initial_state = CFR_State(game, 1)
            self.cfr_recursive(game, initial_state)
            
            if iteration % (self.iterations/10):
                print(f"Completed {iteration}/10 of training")
                print(f"Current strategy: {player1}")

def cfr(state:CFR_State, p0:float, p1:float) -> float:
    """counterfactual regret minimisation"""



    # return payoff for terminal state
