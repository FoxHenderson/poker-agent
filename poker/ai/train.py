from cmdlogic.game import Game
from cmdlogic.card import Card
from cmdlogic.abstracted_actions import AbstractAction
from CFR_player import CFR_Player
import time
from copy import deepcopy
from CFRState import CFR_State
from cmdlogic.actions import Action

import sys

sys.setrecursionlimit(10**6)



# implementation baed on  http://modelai.gettysburg.edu/2013/cfr/cfr.pdf

class CFR_Trainer:
    def __init__(self, iterations:int=10):
        self.iterations = iterations
        
        self.info_sets = {} # maps str -> InformationSet

        self.train()


    def CPUvsCPU(self, game, p1, p2):
        print("START")
        p1.make_move(game, AbstractAction.CALL)
        p2.make_move(game, AbstractAction.FOLD)
        print(game.game_log)
        input()


    def cfr_bhjrecursive(self, game, state, player_to_act):
        if game.ended == True:
            print("\n\n", game.game_log)
            input()
            return game.get_terminal_values()

        possible_actions = player_to_act.valid_actions
        action_values = {}
        expected_value = 0.0
        for action in possible_actions:
            if action == AbstractAction.FOLD and AbstractAction.CHECK in possible_actions:
                action = AbstractAction.CHECK

            game_copy = deepcopy(game)
            player_to_act = game_copy.get_matching_player(player_to_act.ID)
            
            player_to_act.make_move(game_copy, action)
            print()
            state_copy = CFR_State(game_copy, player_to_act.ID)
            
           # game_copy.to_act_index = (game_copy.to_act_index + 1) % len(game_copy.players)
            player_to_act = game_copy.get_opponent_player(player_to_act)
            print("ACTIONCOMPLETER:, ", action, player_to_act.valid_actions)
            action_values[action] = self.cfr_recursive(game_copy, state_copy, player_to_act)
            


    def cfr_recursive(self, game: Game, state: CFR_State):
        #print("RECURSION")
        if state.is_terminal():
           # print("BREAKPOINT")
            t = game.get_terminal_values()
            #print(t)
            print("\n\n",game.game_log)
            input("PRESS ENTER")
            return t
        
        player_to_act = game.players[game.to_act_index]
        possible_actions = player_to_act.valid_actions #state.get_possible_actions()
        print(f"OPTIONS for {player_to_act}:", possible_actions)

        action_values = {}
        expected_value = 0.0
        if AbstractAction.FOLD in possible_actions and AbstractAction.CHECK in possible_actions:
                possible_actions.remove(AbstractAction.FOLD)

        for action in possible_actions:

 
            next_game = deepcopy(game)
            player_to_act = next_game.players[next_game.to_act_index]
            possible_actions = player_to_act.valid_actions
            print(f"Exploring action: {action} from player {player_to_act.name} in round {next_game.game_state}")

            player_to_act.make_move(next_game, action)

            next_player_index = (state.player_id + 1) % len(next_game.players)
            next_game.to_act_index = next_player_index

            next_state = CFR_State(next_game, next_game.to_act_index)
            action_values[action] = self.cfr_recursive(next_game, next_state)



            
        #if AbstractAction.BET_HALF in possible_actions and player_to_act.stack - game.pot//2 < 0:
         #       possible_actions.remove(AbstractAction.BET_HALF)
        #if AbstractAction.BET_POT in possible_actions and player_to_act.stack - game.pot < 0:
         #       possible_actions.remove(AbstractAction.BET_POT)

       # if AbstractAction.RAISE_HALF in possible_actions and player_to_act.stack - game.pot//2 < 0:
        #        possible_actions.remove(AbstractAction.RAISE_HALF)
        #if AbstractAction.RAISE_POT in possible_actions and player_to_act.stack - game.pot < 0:
         #       possible_actions.remove(AbstractAction.RAISE_POT)

        #print("OPTIONS_SIMP:", possible_actions)
        
    def train(self):
        player1 = CFR_Player(0, "Player1")
        player2 = CFR_Player(1, "Player2")
        

        for iteration in range(self.iterations):
            game = Game(player1, player2)
            game.pre_flop()
            #self.CPUvsCPU(game, player1, player2)
            initial_state = CFR_State(game, 1)
            self.cfr_recursive(game, initial_state)
            
            #if iteration % (self.iterations/10):
            print(f"Completed {iteration}/10 of training")
            print(f"Current strategy: {player1}")

def cfr(state:CFR_State, p0:float, p1:float) -> float:
    """counterfactual regret minimisation"""



    # return payoff for terminal state
CFR_Trainer(1)
