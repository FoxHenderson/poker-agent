import random

class Card:
    def __init__(self, ID):
        self.ID = ID
        self.suit = self.__CalculateSuit(ID)
        self.rank = self.__CalculateRank(ID)
        print(self.suit, self.rank)


    def __CalculateSuit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __CalculateRank(self, ID):
        rank = {1: "Ace", 2:"Two", 3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Jack",12:"Queen",13:"King"}
        return rank[((ID - (ID%4)) / 4)+1]


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
