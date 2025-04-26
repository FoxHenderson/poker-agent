from cmdlogic.game import Game
from cmdlogic.card import Card
from cmdlogic.abstracted_actions import AbstractAction
from CFR_player import CFR_Player
import time
from copy import deepcopy
from CFRState import CFR_State
from cmdlogic.actions import Action
from information_set import InformationSet, AbstractActions

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
            


    def cfrfsfa_recursive(self, game: Game, state: CFR_State):
        #print("RECURSION")
        if game.is_terminal():
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
            print(f"Exploring action: {action} from player {player_to_act.name} in round {next_game.game_state}")

            player_to_act.make_move(next_game, action)

            next_player_index = (next_game.to_act_index + 1) % len(next_game.players)
            next_game.to_act_index = next_player_index

            next_state = CFR_State(next_game, next_game.to_act_index)
            action_values[action] = self.cfr_recursive(next_game, next_state)
            

        
    def train(self):
        player1 = CFR_Player(0, "Player1")
        player2 = CFR_Player(1, "Player2")
        

        for iteration in range(self.iterations):
            game = Game(player1, player2)
            game.pre_flop()
            #self.CPUvsCPU(game, player1, player2)
            initial_state = CFR_State(game, 1)
            self.cfr_recursive(game, player1)
            
            #if iteration % (self.iterations/10):
            print(f"Completed {iteration}/10 of training")
            print(f"Current strategy: {player1}")

def cfr(state:CFR_State, game:Game, p0:float, p1:float) -> float:
    """
    counterfactual regret minimisation
    p0 for button player
    p1 for bb player
    """
    STARTING_STACK = 1000 # sigma
    SMALL_BLIND = 10
    BIG_BLIND = 20

    player_to_act = game.players[game.to_act_index]
    btn_player = game.players[game.dealer_button]
    bb_player = game.players[(game.dealer_button + 1) % 2]


    # return payoff for terminal state
    if state.is_terminal():
        stack_dict = game.get_terminal_values()

        # net profit relative to starting stack and blinds posted
        btn_profit = (stack_dict[btn_player] - STARTING_STACK - SMALL_BLIND)
        bb_profit = (stack_dict[bb_player] - STARTING_STACK - BIG_BLIND)

        return btn_profit if btn_player == player_to_act else bb_profit

    # lookup/create info set 
    curr_info_set = InformationSet

    # for each action call cfr with additional history and prob
    strategy = curr_info_set.get_strategy(p0 if player_to_act == btn_player else p1)
    util = [0.0] * AbstractActions.NUM_ACTIONS
    node_util = 0

    possible_actions = state.get_possible_actions()

    action_values = {}
    expected_value = 0.0
    a = 0
    for action in possible_actions:
        next_game = deepcopy(game)
        next_state = CFR_State(next_game, state.player_id)

        if action == AbstractAction.FOLD:
            next_game.fold(player_to_act)
        elif action == AbstractAction.CHECK:
            next_game.check(player_to_act)
        elif action == AbstractAction.CALL:
            next_game.call(player_to_act)
        elif action == AbstractAction.BET_HALF:
            next_game.bet(player_to_act, (state.get_pot()//2))
        elif action == AbstractAction.BET_POT:
            next_game.bet(player_to_act, state.get_pot())
        elif action == AbstractAction.RAISE_HALF:
            next_game.raise_bet(player_to_act, (state.get_pot()//2))
        elif action == AbstractAction.RAISE_POT:
            next_game.raise_bet(player_to_act, state.get_pot())   
        elif action == AbstractAction.ALL_IN:
            next_game.all_in(player_to_act)

        #time.sleep(0.2)
        next_player_id = (state.player_id + 1) % len(next_game.players)#
        next_game.to_act_index = next_player_id
        next_state = CFR_State(next_game, next_player_id)

        if btn_player == player_to_act:
            util[a] =  cfr(next_state, next_game, p0 * strategy[a], p1)
        else:
            util[a] =  cfr(next_state, next_game, p0, p1 * strategy[a])

        nodeUtil += strategy[a] * util[a];
        a += 1

    # for each action, compute counterfactual regret
    a = 0
    for action in possible_actions:
        regret = util[a] - node_util
        curr_info_set.


        a += 1


CFR_Trainer(1)
