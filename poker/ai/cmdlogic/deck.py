import random
from .card import Card

class Deck:
    def __init__(self):
        self.deck = self.__create_deck()
        self.size = len(self.deck)

    def __create_deck(self):
        deck = []
        for i in range(0, 52):
            deck.append(Card(i))
        return deck
            
    def shuffle_deck(self):
        random.shuffle(self.deck)

    def peek(self, index=0) -> Card:
        if index >= len(self.deck) or index < 0:
            return Exception
        return self.deck[index]
    
    def draw_card(self):
        if self.deck:
            card = self.deck.pop()
            self.size -= 1
            return card
        else:
            raise Exception("empty deck")

    def burn_card(self):
        self.deck.pop(self.size-1)
        self.size -= 1
