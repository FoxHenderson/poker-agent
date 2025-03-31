import random
import numpy as np

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
        print(self.suit, self.rank, self.bin)

    def __Calculate_suit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __Calculate_rank(self, ID):
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


class Table:
    def __init__(self):
        self.dealer = 0
        self.deck = Deck()
        self.flop = None
        self.river = None
        self.turn = None

    def reveal_flop(self):
        self.flop = self.deck.draw_card()
    def reveal_river(self):
        self.river = self.deck.draw_card()

    def reveal_rurn(self):
        self.turn = self.deck.draw_card()


    def get_cards(self):
        return(self.flop, self.river, self.turn)


class Players:
    def __init__(self,ID, card1, card2):
        self.ID = ID
        self.card1 = card1
        self.card2 = card2
        self.bid_history = []

    def show_cards(self):
        print (self.card1.rank, "of", self.card1.suit, "(", self.card1.bin, ")", "AND", self.card2.rank, "of", self.card2.suit, "(", self.card2.bin, ")")

    def get_previous_bid():
        return self.bid_history[-1]
class Pot:
    def __init__(self):
        self.value = 0

    def add(self, amount_to_add):
        self.value += amount_to_add

    def clear_pot(self):
        self.value = 0








class Game:
    def __init__(self):
        self.table = Table()
        self.players = self.deal_cards()
        self.pot = Pot()
        self.bigbid = self.players[0]


        self.start_game()



    def start_game(self):
        self.display_cards()
        self.bidding_round(self.bigbid)



    def get_bid_amount(self):
        value = int(input("Bid Value:"))
        return value


    def get_choice(self):
        return input("Bid or Fold or Increase (b, f, i)")



    def bidding_round(self, current_bidder):
        print(current_bidder.ID)
        bid_amount=self.get_bid_amount()
        self.pot.add(bid_amount)

        for player in self.players:
                if player != current_bidder:
                    print(player.ID)
                    choice = self.get_choice()
                    if choice == "b":
                        self.pot.add(bid_amount)
                    elif choice == "f":
                        self.players.remove(player)
                        player.show_cards()
                    elif choice == "i":
                        self.bidding_round(player)
                    
            
        

    def deal_cards(self):
        players_num = 2
        players = []
        for i in range(0, players_num):
            p = Players(f"player_{i+1}",self.table.deck.draw_card(), self.table.deck.draw_card())
            players.append(p)
        return players


    def display_cards(self):
        for p in range(0, len(self.players)-1):

            print("PLAYER {p}:")
            self.players[p].show_cards()
            print("\n")

        computer = self.players[-1]
        print("COMPUTER CARDS")
        computer.show_cards()
        print("\n\n")




def __main__():
    return Game()


    
cheese = Game()
