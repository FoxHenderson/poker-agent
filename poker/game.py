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

        self.board = []

        self.action_history = []

        # blinds
        self.big_blind = 20
        self.small_blind = 10

        # index of dealer button. (0 or 1)
        self.dealer_button = 0

        # pre-flop = 0, flop = 1, turn = 2, river = 3
        self.game_state = 0

    def game_loop(self):
        self.deal_cards()

        # ========= pre-flop =========
        winner = self.betting_loop(self.dealer_button)
        if winner: # game is over
            winner.stack += self.pot
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1
        
        # ========= flop =========
        self.deal_flop()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # ========= turn =========
        self.deal_turn()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # ========= river =========
        self.deal_river()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # determine winnner
        self.determine_winner()

    def betting_loop(self, to_act_index:int):
        """returns False if game should continue else returns the winner (player obj)"""

        last_action = (None, 0)

        # handle blinds
        if self.game_state == 0:
            self.players[self.dealer_button].bet = self.small_blind
            self.players[self.dealer_button].stack -= self.small_blind

            self.players[(self.dealer_button + 1) % 2].bet = self.big_blind
            self.players[(self.dealer_button + 1) % 2].stack -= self.big_blind

            self.pot += self.big_blind + self.small_blind

            last_action = (Action.RAISE, self.big_blind)

        # if a player is all in skip the betting round
        for player in self.players:
            if player.all_in:
                return False

        # betting loop
        while True:
            hero_player = self.players[to_act_index]
            villain_player = self.players[(to_act_index + 1) % 2]

            call_amount = villain_player.bet - hero_player.bet

            current_action, current_amount = hero_player.action(last_action, call_amount)

            if current_action == Action.FOLD: # terminating action
                return villain_player
            elif current_action == Action.CHECK:
                if last_action[0] == Action.CHECK: # terminating action (checks round)
                    return False
            elif current_action == Action.CALL: # terminating action
                self.pot += call_amount
                hero_player.stack -= call_amount
                return False
            elif current_action == Action.BET:
                self.pot += current_amount
                hero_player.bet += current_amount
                hero_player.stack -= (current_amount - self.bet)
            elif current_action == Action.RAISE:
                self.pot += current_amount
                hero_player.stack -= current_amount
                hero_player.bet += current_amount
            elif current_action == Action.ALL_IN:
                hero_player.all_in = True
                last_bet_amt = last_action[1]
                # if the last bet was more than our stack (terminating case)
                if last_bet_amt > current_amount:
                    difference = last_bet_amt - current_amount
                    # credit villain the difference
                    villain_player += difference
                    self.pot -= difference

                    self.pot += current_amount
                    hero_player.bet += current_amount
                    hero_player.stack -= current_amount

                    return False
                # == case is coverered in selection logic (converted to call)
                # < case, continue betting as normal 
                hero_player.bet += current_amount
                self.pot += current_amount
                hero_player.stack -= current_amount

            last_action = (current_action, current_amount)
            to_act_index = (to_act_index + 1) % 2

    def update_dealer_button(self):
        self.dealer_button = (self.dealer_button + 1) % 2

    def deal_cards(self):
        for _ in range(2):
            for i in range(2):
                (self.players[(self.dealer_button + i) % 2].cards).append(self.deck.draw_card())

    def determine_winner(self):
        winner = None

        hand_strength = []
        for i in range(len(self.players)):
            score = eval_seven_card(self.board + (self.players[i]).cards)
            hand_strength[i] = score
        
        # draw
        if hand_strength[0] == hand_strength[1]:
            self.resolve_draw()
            return
        elif hand_strength[0] < hand_strength[1]:
            winner = self.players[0]
        else:
            winner = self.players[1]

        winner.stack += self.pot

        return

    def resolve_draw(self):
        # if pot is odd, give spare to player on dealer button
        # seems to be large number of ways this can be split (this was the easiest to implement lol)
        if self.pot % 2 == 1:
            self.players[self.dealer_button].stack += 1
            self.pot -= 1

        self.players[0].stack += (self.pot / 2)
        self.players[1].stack += (self.pot / 2)

    def deal_flop(self):
        self.deck.burn_card()
        for i in range(3):
            new_card = self.deck.draw_card()
            self.board.append(new_card)

    def deal_turn(self):
        self.deck.burn_card()
        self.board.append(self.deck.draw_card())

    def deal_river(self):
        self.deck.burn_card()
        self.board.append(self.deck.draw_card())

    def end_round(self):
        for player in self.players:
            player.bet = 0

    def reset(self):
        for player in self.players:
            player.action_history = [[], [], [], []]
            player.bet = 0
            player.cards = []
            player.folded = False
            player.all_in = False
        
        self.board = []
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.pot = 0
        self.game_state = 0

        # index of dealer button. (0 or 1)
        self.dealer_button = (self.dealer_button + 1) % 2

# used to interface with the GUI
class GUI_Game(Game):
    """Used to interface with the GUI"""
    def game_loop(self):
        return super().game_loop()

# play poker in the command line
class CL_Game(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
    
    def game_loop(self):
        self.deal_cards()

        # ========= pre-flop =========
        winner = self.betting_loop(self.dealer_button)
        if winner: # game is over
            winner.stack += self.pot
            print(f"{winner.name} wins.")
            for player in self.players:
                print(player)

            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1
        
        # ========= flop =========
        self.deal_flop()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot

            print(f"{winner.name} wins.")
            for player in self.players:
                print(player)
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # ========= turn =========
        self.deal_turn()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot

            print(f"{winner.name} wins.")
            for player in self.players:
                print(player)
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # ========= river =========
        self.deal_river()

        winner = self.betting_loop((self.dealer_button + 1) % 2)
        if winner: # game is over
            winner.stack += self.pot

            print(f"{winner.name} wins.")
            for player in self.players:
                print(player)
            # round over
            self.reset()
            return
        self.end_round()
        self.game_state += 1

        # determine winnner
        self.determine_winner()

    def betting_loop(self, to_act_index:int):
        """returns False if game should continue else returns the winner (player obj)"""

        last_action = (None, 0)

        # handle blinds
        if self.game_state == 0:
            print(f"{self.players[self.dealer_button].name} posts small blind ({self.small_blind})")
            self.players[self.dealer_button].bet = self.small_blind
            self.players[self.dealer_button].stack -= self.small_blind

            print(f"{self.players[(self.dealer_button + 1) % 2].name} posts big blind ({self.big_blind})")
            self.players[(self.dealer_button + 1) % 2].bet = self.big_blind
            self.players[(self.dealer_button + 1) % 2].stack -= self.big_blind

            self.pot += self.big_blind + self.small_blind

            last_action = (Action.RAISE, self.big_blind)

        # if a player is all in skip the betting round
        for player in self.players:
            if player.all_in:
                return False

        # betting loop
        while True:
            hero_player = self.players[to_act_index]
            villain_player = self.players[(to_act_index + 1) % 2]

            call_amount = villain_player.bet - hero_player.bet

            current_action, current_amount = hero_player.action(last_action, call_amount)

            print(f"{hero_player.name} {current_action} ({current_amount})")

            if current_action == Action.FOLD: # terminating action
                return villain_player
            elif current_action == Action.CHECK:
                if last_action[0] == Action.CHECK: # terminating action (checks round)
                    return False
            elif current_action == Action.CALL: # terminating action
                self.pot += call_amount
                hero_player.stack -= call_amount
                return False
            elif current_action == Action.BET:
                self.pot += current_amount
                hero_player.bet += current_amount
                hero_player.stack -= (current_amount - self.bet)
            elif current_action == Action.RAISE:
                self.pot += current_amount
                hero_player.stack -= current_amount
                hero_player.bet += current_amount
            elif current_action == Action.ALL_IN:
                hero_player.all_in = True
                last_bet_amt = last_action[1]
                # if the last bet was more than our stack (terminating case)
                if last_bet_amt > current_amount:
                    difference = last_bet_amt - current_amount
                    # credit villain the difference
                    villain_player += difference
                    self.pot -= difference

                    self.pot += current_amount
                    hero_player.bet += current_amount
                    hero_player.stack -= current_amount

                    return False
                # == case is coverered in selection logic (converted to call)
                # < case, continue betting as normal 
                hero_player.bet += current_amount
                self.pot += current_amount
                hero_player.stack -= current_amount

            print(f"{villain_player.name}'s turn. {current_amount - villain_player.bet} to call")

            last_action = (current_action, current_amount)
            to_act_index = (to_act_index + 1) % 2

    def deal_cards(self):
        for _ in range(2):
            for i in range(2):
                (self.players[(self.dealer_button + i) % 2].cards).append(self.deck.draw_card())

        for player in self.players:
            print(f"{player.name}:")
            player.show_hand()

    def deal_flop(self):
        super().deal_flop()
        self.print_board()

    def print_board(self):
        print("Board:") 
        print(self.board)

    def deal_turn(self):
        super().deal_turn()
        self.print_board()

    def deal_river(self):
        super().deal_river()
        self.print_board()

    def determine_winner(self):
        winner = None

        hand_strength = []
        for i in range(len(self.players)):
            score = eval_seven_card(self.board + (self.players[i]).cards)
            hand_strength.append(score)
        
        # draw
        if hand_strength[0] == hand_strength[1]:
            self.resolve_draw()
            return
        # recall low score is better!
        elif hand_strength[0] < hand_strength[1]:
            winner = self.players[0]
        else:
            winner = self.players[1]

        for score in hand_strength:
            print(score)

        winner.stack += self.pot
        print(f"{winner.name} wins.")
        for player in self.players:
            print(player)

        return