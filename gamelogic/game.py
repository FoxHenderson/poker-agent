import random
import numpy as np

# constants
BIN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
BIN_SUITS = [1, 2, 4, 8]

class Card:
    def __init__(self, ID):
        # ID unique integer from 1 - 52
        self.ID = ID
        # suit, rank string representation
        self.suit = self.__CalculateSuit(ID)
        self.rank = self.__CalculateRank(ID)
        # binary representation of the card, used for the agents internal representation of the game
        self.bin = self.__CalculateBin(ID)

        # debug --------
        print(self.suit, self.rank, self.bin)

    def __CalculateSuit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    # convention to have ace high
    def __CalculateRank(self, ID):
        rank = {1:"Two", 2:"Three",3:"Four",4:"Five",5:"Six",6:"Seven",7:"Eight",8:"Nine",9:"Ten",10:"Jack",11:"Queen",12:"King",13: "Ace", }
        return rank[((ID - (ID%4)) / 4)+1]

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
        suit = (1 << (ID % 13)) << 12
        bit = (2**(ID // 4)) << 16
        return (prime | rank | suit | bit)

class Deck:
    def __init__(self):
        self.deck = self.__createDeck()
        self.size = len(self.deck)
    def __createDeck(self):
        deck = []
        print("DECK: ", deck)
        for i in range(0, 52):
            deck.append(Card(i))
        return deck
            
    def drawCard(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        self.size -= 1
        return card


class Table:
    def __init__(self):
        self.dealer = 0
        self.deck = Deck()
        self.flop = None
        self.river = None
        self.turn = None

    # we need to reveal three cards here
    def revealFlop(self):
        self.flop = self.deck.drawCard()

    def revealRiver(self):
        self.river = self.deck.drawCard()

    def revealTurn(self):
        self.turn = self.deck.drawCard()


    def showCentreCards(self):
        return(self.flop, self.river, self.turn)


class PlayerHoles:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2

    def showCards(self):
        return (self.card1.rank + self.card1.suit), (self.card2.rank + self.card2.suit)
        


class Game:
    def __init__(self):
        self.table = Table()
        self.players = self.dealCards()

    def dealCards(self):
        players_num = 2
        player_holes = []
        for i in range(0, players_num):
            p = PlayerHoles(self.table.deck.drawCard(), self.table.deck.drawCard())
            p.showCards()
            player_holes.append(p)
        return player_holes
    

# test the binary mibibble
def test_mabibble():
    cheeky_deck = Deck()
    for card in cheeky_deck.deck:
        #print(bin(card.bin))
        ...

test_mabibble()