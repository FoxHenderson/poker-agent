from fivecardeval import evalFromBin
from gamelogic.game import Deck, Card

EXPECTED_FREQUENCY = [
        0, 40, 624, 3744, 5108, 10200, 54912, 123552, 1098240, 1302540
]


# tests the five card evaluation on every possible combination of five cards
def test_five_card():
    
    testDeck = Deck()

    # O(n^5) moment
    for a in range(0, 48):
        for b in range(0, 49):
            for c in range(0, 50):
                for d in range(0, 51):
                    for e in range(0, 52):
                        hand = [
                                testDeck.deck[a], 
                                testDeck.deck[b], 
                                testDeck.deck[c], 
                                testDeck.deck[d], 
                                testDeck.deck[e]     
                                ]
                        
                        handBin = (card.__CalculateBin() for card in hand)

                        assert(
                            evalFromBin(handBin[0], handBin[1], handBin[2], handBin[3], handBin[4]) ==
                            99
                        )