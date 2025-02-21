from gamelogic.card import Card

# based on the method described at http://suffe.cool/poker/evaluator.html

# +--------+--------+--------+--------+
# |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
# +--------+--------+--------+--------+
# p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
# r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
# cdhs = suit of card (bit turned on based on suit of card)
# b = bit turned on depending on rank of card

# takes an input of 5 card objects returns an integer 1-7462 representing a hands ranking, with 
# 1 being the best hand type (all royal flushes) 
# and 7462 being the worst (75432o)

def evaluateFiveCardFromCardObj(Cards : list[Card]) -> int:
    ...
    return evaluateFiveCardFromBin(...)

def evaluateFiveCardFromBin(Cards : list[int]) -> int:
    ...
    return -1

# takes a card object as an input, converts it to a 4 byte binary number for calculations
def convertCardObjToInt(card : Card) -> int:
    ...