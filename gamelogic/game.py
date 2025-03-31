import random

class Card:
    def __init__(self, ID):
        self.ID = ID
        self.suit = self.__Calculate_suit(ID)
        self.rank = self.__Calculate_rank(ID)
        #print(self.suit, self.rank)


    def __Calculate_suit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __Calculate_rank(self, ID):
        rank = {1: "Ace", 2:"Two", 3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Jack",12:"Queen",13:"King"}
        return rank[((ID - (ID%4)) / 4)+1]


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


class PlayerHoles:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2

    def show_cards(self):
        return (self.card1.rank + self.card1.suit), (self.card2.rank + self.card2.suit)
        


class Game:
    def __init__(self):
        self.table = Table()
        self.players = self.deal_cards()

    def deal_cards(self):
        players_num = 2
        player_holes = []
        for i in range(0, players_num):
            p = PlayerHoles(self.table.deck.draw_card(), self.table.deck.draw_card())
            p.show_cards()
            player_holes.append(p)
        return player_holes



def __main__():
    return Game()




