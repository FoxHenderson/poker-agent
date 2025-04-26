import random
#import numpy as np

from .evaluation.handeval import eval_seven_card
from .deck import Deck
from .player import Player
from .actions import Action

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
        self.ended = False

        """ACTION ASSOCIATED ATTRIBUTES"""
        self.checkstate = 0 # 0 is no-body has checked, 1 is when one player has checked, 2 is when both players choose to check
        self.previous_bet_amount = 0
        self.to_act_index = 0 # DETERMINES WHAT PLAYERS TURN IT IS
        self.round_name = ""
        self.previous_player = ""
        self.deal_cards()


# UTILITY FUNCTIONS]
    def update_game_log(self, log):
        self.game_log = self.game_log + "\n" + str(log)


    def get_opponent_player(self, player):
        for p in self.players:
            if p.ID != player.ID:
                return p
        return False

    def update_dealer_button(self):
        self.dealer_button = (self.dealer_button + 1) % 2

    def switch_player(self):
        self.to_act_index = (self.to_act_index + 1) % 2

    def get_round_name(self):
        if self.game_state == 0:
            print("PREFLOP")
            self.update_game_log("Pre-Flop Round:")
            self.round_name = "Pre-Flop"
        elif self.game_state == 1:
            print("FLOP")
            self.deal_flop()
            self.update_game_log("Flop Round:")
            self.round_name = "Flop"
        elif self.game_state == 2:
            print("TURN")
            self.deal_turn()
            self.update_game_log("Turn Round:")
            self.round_name = "Turn"
        elif self.game_state == 3:
            print("FIVER")
            self.deal_river()
            self.update_game_log("River Round:")
            self.round_name = "River"
        else:
            self.determine_winner()
            self.update_game_log(str(str(self.winner) + " WINS"))
            return False
            print("GAME OVER")
        return self.round_name

    def check_for_winner(self):
        """CHECK FOR WINNER"""
        if self.loser != False:
            print(self.get_opponent_player(self.loser).name, " WINS")
            self.winner = self.get_opponent_player(self.loser)
            return True



#CFR
    def is_hand_over(self) -> bool:
        return self.loser != False or self.game_state > 3 or self.ended

    def get_terminal_values(self) -> dict[Player, int]:
        terminal_values = {}
        for player in self.players:
            terminal_values[player] = player.stack
        return terminal_values

    def get_last_action(self):
        return self.action_history[-1]

    def get_matching_player(self, playerID):
        for p in self.players:
            if p.ID == playerID:
                return p
        


# GAME FUNCTIONS

    def deal_cards(self):
        for _ in range(2):
            for i in range(2):
                card = self.deck.draw_card()
                (self.players[(self.dealer_button + i) % 2].cards).append(card)


    def next_round(self):
        for player in self.players:
            player.bet = 0
        if self.winner: # game is over
            self.winner.stack += self.pot
            return
        self.game_state +=1
        print("self.game_state:", self.game_state)
        return self.get_round_name()
            


    def determine_winner(self):
        winner = None

        hand_strength = {}
        for i in range(len(self.players)):
            score = eval_seven_card(self.board + (self.players[i]).cards)
            hand_strength[i] = score
        
        # draw
        if hand_strength[0] == hand_strength[1]:
            self.resolve_draw()
            return
        elif hand_strength[0] < hand_strength[1]:
            self.winner = self.players[0]
        else:
            self.winner = self.players[1]


        print("STRENGTHS:", hand_strength)
        self.winner.stack += self.pot

        self.end_game()
        return hand_strength


    def resolve_draw(self):
        # if pot is odd, give spare to player on dealer button
        # seems to be large number of ways this can be split (this was the easiest to implement lol)
        if self.pot % 2 == 1:
            self.players[self.dealer_button].stack += 1
            self.pot -= 1

        self.players[0].stack += (self.pot / 2)
        self.players[1].stack += (self.pot / 2)    


    def end_game(self):
        self.ended = True
        self.update_game_log(("FINAL STANDINGS:", str(self.players[0]), str(self.players[1])))
        self.update_game_log("END OF GAME!")

        #self.restart()

    def restart(self):
        self.update_game_log("RESTARTING!")
        for player in self.players:
            player.action_history = [[], [], [], []]
            player.bet = 0
            player.cards = []
            player.folded = False
            player.all_in = False

        self.board = [None]*5
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.pot = 0
        self.game_state = 0
        self.winner = False

        # index of dealer button. (0 or 1)
        self.dealer_button = (self.dealer_button + 1) % 2

        self.deal_cards()
        self.pre_flop()




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





# GAME ACTIONS

    def fold(self, player):
        other_player = self.get_opponent_player(player)
        self.checkstate = 0
        print(player.name, "loses")
        player.folded = True
        self.winner = other_player
        self.winner.stack += self.pot
        self.pot = 0
        player.action_history[self.game_state].append((Action.FOLD, 0))


        other_player.update_available_actions((Action.FOLD, 0))
        
        player.update_available_actions((Action.FOLD, 0))
        self.update_game_log(f"{player} Folded")

        self.previous_player = player
        self.end_game()

    
    def check(self, player):
        other_player = self.get_opponent_player(player)
        self.checkstate+=1
        self.update_game_log(f"{player} Checked")
        player.action_history.append((Action.CHECK, 0))
        other_player.update_available_actions((Action.CHECK, 0))
        if self.checkstate == 2:
            self.checkstate = 0
            self.update_dealer_button()
            self.update_game_log(f"Players agreed to check")
            player.add_bet(0)

            self.previous_player = player
            self.next_round()
            return True
        else:
            self.previous_player = player
            return False

    def call(self, player):
        other_player = self.get_opponent_player(player)
        call_amount = abs(other_player.bet - player.bet)
        self.pot += call_amount
        player.stack -= call_amount
        self.checkstate = 0

        player.add_bet(call_amount)
        player.action_history[self.game_state].append((Action.CALL, call_amount))
        other_player.update_available_actions((Action.CALL, call_amount))
        
        self.update_game_log(f"{player} Called (added {call_amount})")

        self.previous_player = player
        self.next_round()
        return True

    def bet(self, player, amount_to_bet):
        other_player = self.get_opponent_player(player)

        if player.stack - amount_to_bet < 0 :
            print("BIG FAT AND FALSE")
            return False
        
        self.pot += amount_to_bet
        player.bet += amount_to_bet
        player.stack -= amount_to_bet # PLEASE REVIEW THIS LINE TO SEE IF IT IS DOING THE CORRECT THING
        self.checkstate = 0
        player.add_bet(amount_to_bet)
        player.action_history[self.game_state].append((Action.BET, amount_to_bet))
        other_player.update_available_actions((Action.BET, amount_to_bet))
        self.update_game_log(f"{player} Betted {amount_to_bet}")
        self.previous_player = player
        return True

    def raise_bet(self, player, amount_to_raise):
        other_player = self.get_opponent_player(player)
        self.checkstate = 0
        if amount_to_raise <= other_player.previous_bet or player.stack - amount_to_raise < 0 :
            print("BIG FAT AND FALSE")
            return False
        else:
            self.pot += amount_to_raise
            player.stack -= amount_to_raise
            player.bet += amount_to_raise

            player.add_bet(amount_to_raise)
            player.action_history[self.game_state].append((Action.RAISE, amount_to_raise))
            other_player.update_available_actions((Action.RAISE, amount_to_raise))
            
            self.update_game_log(f"{player} Raised ({amount_to_raise})")
            self.previous_player = player
            return True


    def all_in(self, player):
        """NEED TO FINALISE HOW THIS FUNCTION WORKS - DISCUSS WITH FOX"""
        self.checkstate = 0
        player.all_in = True
        other_player = self.get_opponent_player(player)
        last_bet_amt = other_player.previous_bet
        bet_amt = player.stack
        # if the last bet was more than our stack (terminating case)
        if last_bet_amt > player.stack:
                    difference = last_bet_amt - player.stack
                    # credit villain the difference
                    other_player.stack += difference
                    self.pot -= difference
                    
                    last_bet_amt
                    self.pot += bet_amt
                    player.bet += bet_amt
                    player.stack -= bet_amt
                    player.add_bet(bet_amt)

                    self.next_round()
        else:
            # == case is coverered in selection logic (converted to call)
            # < case, continue betting as normal 
            player.bet += bet_amt
            self.pot += bet_amt
            player.stack -= bet_amt
            player.add_bet(bet_amt)


        player.action_history[self.game_state].append((Action.ALL_IN,player.stack))
        other_player.update_available_actions((Action.ALL_IN, player.stack))
        self.update_game_log(f"{player} went All In")
        self.previous_player = player
        
