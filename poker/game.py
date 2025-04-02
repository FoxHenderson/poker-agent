import random
import numpy as np
from enum import Enum


from evaluation.handeval import eval_seven_card
from card import Card
from deck import Deck
from player import Player

# constants
BIN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
BIN_SUITS = [1, 2, 4, 8]

class Action(Enum):
    Fold = 1,
    Check = 2,
    Call = 3,
    Raise = 4,
    AllIn = 5,

    def get_actions(self):
        if self == Action.Check:
            return [Action.Check, Action.Call, Action.Raise, Action.Fold]
        elif self == Action.Raise:
            return [Action.Fold, Action.Call, Action.Raise]
        elif self == Action.AllIn:
            return [Action.Fold, Action.Call]


class Game:
    def __init__(self, player1:Player, player2:Player):
        self.deck = Deck()
        self.deck.shuffle_deck()

        self.players = [player1, player2]
        self.pot = 0

        self.board = []

        # blinds
        self.big_blind = 20
        self.small_blind = 10

        # index of dealer button. (0 or 1)
        self.dealer_button = 0

    def game_loop(self):
        self.deal_cards()
        # update GUI with cards

        # ========= pre-flop =========

        # ========= flop =========
        self.betting_loop()

        # ========= turn =========


        # ========= river =========


        # determine winnner
        hand_strength = []
        for i in range(len(self.players)):
            score = eval_seven_card(self.board + (self.players[i]).cards)
            hand_strength[i] = score
        
        # draw
        if hand_strength[0] == hand_strength[1]:
            self.resolve_draw()
        elif hand_strength[0] > hand_strength[1]:
            self.resolve_winner(self.players[0])
        else:
            self.resolve_winner(self.players[1])

    def betting_loop(self, to_act_index, state, current_bet=0):
        last_raiser = None
        players_acted = [False, False]
        
        while players_acted != [True, True]:
            curr_player = self.players[to_act_index]

    def update_dealer_button(self):
        self.dealer_button = (self.dealer_button + 1) % 2

    def deal_cards(self):
        for _ in range(2):
            for i in range(2):
                (self.players[(self.dealer_button + i) % 2].cards).append(self.deck.draw_card())

    def resolve_winner(self, player:Player):
        ...

    def resolve_draw(self):
        # if pot is odd, give spare to player on dealer button
        # seems to be large number of ways this can be split (this was the easiest to implement lol)
        if self.pot % 2 == 1:
            self.players[self.dealer_button].stack += 1
            self.pot -= 1

        self.players[0].stack += (self.pot / 2)
        self.players[1].stack += (self.pot / 2)

    def deal_flop(self):
        for _ in range(3):
            self.board.append(self.deck.draw_card())

    def deal_turn(self):
        self.board.append(self.deck.draw_card())

    def deal_river(self):
        self.board.append(self.deck.draw_card())

    def reset():
        ...


# Testing

user = Player(0, "J.W", 0)
computer = Player(1, "Computer", 1)

test_game = Game(user, computer)
while (user.stack > 0) and (computer.stack > 0):
    test_game.game_loop() 