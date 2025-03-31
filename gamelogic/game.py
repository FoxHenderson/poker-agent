import random
import numpy as np
from enum import Enum

# constants
BIN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
BIN_SUITS = [1, 2, 4, 8]

class Card:
    def __init__(self, ID):
        # ID unique integer from 1 - 52
        self.ID = ID
        self.suit = self.__Calculate_suit(ID)
        self.rank = self.__Calculate_rank(ID)
        # binary representation of the card, used for the agents internal representation of the game
        self.bin = self.__CalculateBin(ID)
        self.bin = format(self.bin, '#034b')

        # debug --------
        #print(self.suit, self.rank, self.bin)

    def __Calculate_suit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __Calculate_rank(self, ID):
        rank = {1:"Two", 2:"Three",3:"Four",4:"Five",5:"Six",6:"Seven",7:"Eight",8:"Nine",9:"Ten",10:"Jack",11:"Queen",12:"King",13: "Ace", }
        return rank[((ID - (ID%4)) / 4)+1]

    def show_card(self):
        return f"{self.rank} of {self.suit}"

    # returns card as binary number
    #+--------+--------+--------+--------+
    #|xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
    #+--------+--------+--------+--------+
    #p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
    #r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
    #cdhs = suit of card (bit turned on based on suit of card)
    #b = bit turned on depending on rank of card

    def __CalculateBin(self, ID):
        # sum maffs
        prime = BIN_PRIMES[ID // 4]
        rank = (ID // 4) << 8
        suit = (1 << (ID % 4)) << 12
        bit = (2**(ID // 4)) << 16
        return (prime | rank | suit | bit)

class Deck:
    def __init__(self):
        self.deck = self.__create_deck()
        self.size = len(self.deck)

    def __create_deck(self):
        deck = []
        #print("DECK: ", deck)
        for i in range(0, 52):
            deck.append(Card(i))
        return deck
            
    def draw_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        self.size -= 1
        return card

class Player:
    def __init__(self, ID, name, mode):
        self.ID = ID
        self.name = name
        self.card1 = None
        self.card2 = None
        self.stack = 1000

        # 0: manual player, 1: random action, 2: AI
        self.mode = mode

        # pre-flop, flop, turn, river
        # actions of the form: f - fold, cx - call $x, rx - raise $x 
        self.action_history = [[], [], [], []]

    def show_cards(self):
        print (" ", self.card1.show_card(), "\n ", self.card2.show_card())

    def get_previous_bid(self):
        for i in range(3, -1, -1):
            if len(self.action_history[i]) == 0:
                continue
            return self.action_history[i][-1]
        return None    
    
    def update_action(self, last_action:Enum, state):
        # preflop = 0, flop = 1, turn = 2, river = 3
        self.action_history[state].append(last_action)

    def get_last_action(self, state):
        if len(self.action_history[state]) > 0:
            return self.action_history[state][-1]
        return None
        
class Action(Enum):
    Fold = 1,
    Check = 2,
    Call = 3,
    Raise = 4,

    def get_actions(self):
        if self == Action.Check:
            return [Action.Check, Action.Call, Action.Raise, Action.Fold]
        elif self == Action.Raise:
            return [Action.Fold, Action.Call, Action.Raise]


class Game:
    def __init__(self, player1, player2):
        self.deck = Deck()
        self.players = [player1, player2]
        self.pot = 0

        # blinds
        self.big_blind = 20
        self.small_blind = 10

        # index of dealer button. (0 or 1)
        self.dealer_button = 0

    def game_loop(self):
        # pre flop: dealer button is small blind
        ...

    def betting_loop(self, to_act_index, current_bet=0):
        last_raiser = None
        players_acted = [False, False]
        
        while players_acted != [True, True]:
            curr_player = self.players[to_act_index]


    def update_dealer_button(self):
        self.dealer_button = (self.dealer_button + 1) % 2

    def deal_cards(self):
        for player in self.players:
            player.hand.append()