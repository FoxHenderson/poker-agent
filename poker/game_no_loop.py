import random
#import numpy as np

from evaluation.handeval import eval_seven_card
from deck import Deck
from player import Player
from actions import Action











class Game:
    def __init__(self, player1:Player, player2:Player):
        self.deck = Deck()
        self.deck.shuffle_deck()

        self.players = [player1, player2]
        self.pot = 0

        self.board = [None]*5

        self.action_history = []

        # blinds
        self.big_blind = 20
        self.small_blind = 10

        # index of dealer button. (0 or 1)
        self.dealer_button = 0

        # pre-flop = 0, flop = 1, turn = 2, river = 3
        self.game_state = 0
        self.loser = False
        self.winner = False
        self.game_log = "Welcome to Poker!"



        self.done_flop = False
        self.done_turn = False
        self.done_river = False

        """ACTION ASSOCIATED ATTRIBUTES"""
        self.checkstate = 0 # 0 is no-body has checked, 1 is when one player has checked, 2 is when both players choose to check
        self.previous_bet_amount = 0
        self.to_act_index = 0 # DETERMINES WHAT PLAYERS TURN IT IS
        self.round_name = ""

        self.deal_cards()

    def update_game_log(self, log):
        self.game_log = self.game_log + "\n" + str(log)


    def get_opponent_player(self, player):
        for p in self.players:
            if p != player:
                return p
        return False


    def deal_cards(self):
        for _ in range(2):
            for i in range(2):
                card = self.deck.draw_card()
                (self.players[(self.dealer_button + i) % 2].cards).append(card)

    def check_for_winner():
        """CHECK FOR WINNER"""
        if self.loser != False:
            print(get_opponent_player(self.loser).name, " WINS")
            self.winner = get_opponent_player(self.loser)
            return True

    def switch_player(self):
        self.to_act_index = (self.to_act_index + 1) % 2


    def get_round_name(self):
        if self.game_state == 0:
            print("PREFLOP")
            self.round_name = "Pre-Flop"
        elif self.game_state == 1:
            print("FLOP")
            self.deal_flop()
            self.round_name = "Flop"
        elif self.game_state == 2:
            print("TURN")
            self.deal_turn()
            self.round_name = "Turn"
        elif self.game_state == 3:
            print("FIVER")
            self.deal_river()
            self.round_name = "River"
        else:
            print("GAME OVER")
        return self.round_name

    def next_round(self):
        for player in self.players:
            player.bet = 0
        if self.winner: # game is over
            winner.stack += self.pot
            return
        self.game_state +=1
        print("self.game_state:", self.game_state)
        return self.get_round_name()
            


    def fold(self, player):
        other_player = self.get_opponent_player(player)
        
        print(player.name, "loses")
        player.folded = True
        self.winner = other_player
        self.winner.stack += self.pot
        self.pot = 0
        player.action_history.append((Action.FOLD, 0))


        other_player.update_available_actions((Action.FOLD, 0))
        player.update_available_actions((Action.FOLD, 0))
        
        self.update_game_log(f"{player.name} Folded")
        return True

    
    def check(self, player):
        
        self.checkstate+=1
        if self.checkstate == 2:
            self.checkstate = 0
            self.update_dealer_button
            next_round()
            player.action_history.append((Action.CHECK, 0))
            self.update_game_log(f"{player.name} Checked")
            self.next_round()
            return True
        else:
            return False

    def call(self, player):
        other_player = self.get_opponent_player(player)
        call_amount = other_player.bet - player.bet
        self.pot += call_amount
        player.stack -= call_amount

        
        player.action_history.append((Action.CALL, call_amount))
        other_player.update_available_actions((Action.CALL, call_amount))
        
        self.update_game_log(f"{player.name} Called (added {call_amount})")

        self.next_round()
        return True

    def bet(self, player, amount_to_bet):
        other_player = self.get_opponent_player(player)        
        self.pot += amount_to_bet
        player.bet += amount_to_bet
        player.stack -= amount_to_bet # PLEASE REVIEW THIS LINE TO SEE IF IT IS DOING THE CORRECT THING

        player.action_history.append((Action.BET, amount_to_bet))
        other_player.update_available_actions((Action.BET, amount_to_bet))
        self.update_game_log(f"{player.name} Betted {amount_to_bet}")

    def raise_bet(self, player, amount_to_raise):
        other_player = self.get_opponent_player(player)
        last_move= other_player.action_history[-1]
        if amount_to_raise < last_move[1]:
            return False
        self.pot += amount_to_raise
        player.stack -= amount_to_raise
        player.bet += amount_to_raise
        player.action_history.append((Action.RAISE, amount_to_raise))
        other_player.update_available_actions((Action.RAISE, amount_to_raise))
        self.update_game_log(f"{player.name} Raised ({amount_to_raise})")


    def all_in(self, player):
        """NEED TO FINALISE HOW THIS FUNCTION WORKS - DISCUSS WITH FOX"""
        player.all_in = True
        player.action_history.append((Action.ALL_IN, 0))
        self.update_game_log(f"{player.name} went All In")


    


    def deal_flop(self):
        self.deck.burn_card()
        for i in range(3):
            new_card = self.deck.draw_card()
            self.board.append(new_card)
        self.board = self.board[3:]

    def deal_turn(self):
        print("TURNING")
        self.deck.burn_card()
        self.board.append(self.deck.draw_card())
        self.board = self.board[1:]

    def deal_river(self):
        self.deck.burn_card()
        self.board.append(self.deck.draw_card())
        self.board = self.board[1:]





    def pre_flop(self):
        self.bet(self.players[self.dealer_button], self.small_blind)
        self.raise_bet(self.players[(self.dealer_button + 1) % 2], self.big_blind)

