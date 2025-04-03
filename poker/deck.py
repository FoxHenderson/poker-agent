import random
from card import Card

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
            
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def draw_card(self):
        card = self.deck.pop()
        self.size -= 1
        return card

    def burn_card(self):
        self.deck.pop()
        self.size -= 1