import evallookup as ev
import unsuited_lookup as ul
import numpy as np
import itertools
#from gamelogic.game import Card

# used for the hand evalutation phase of the poker game logic
#def get5cardRanking(cards : list[Card]) -> int:
#    if len(cards) != 5:
#        raise IndexError
    
#    evalFromBin(cards[0].bin, cards[1].bin, cards[2].bin, cards[3].bin, cards[4].bin)

def eval_from_bin(c:list):
    """Based on the method described at http://suffe.cool/poker/evaluator.html
    takes an input of binary card representations returns an integer 1-7462"""

    primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41 ]

    q = (c[0] | c[1] | c[2] | c[3] | c[4])
    q = q >> 16

    # check flushes
    if (c[0] & c[1] & c[2] & c[3] & c[4] & 0xF000):
        return ev.flushes[q]
    
    # check straights and high card
    s = ev.unique5[q]
    if (s):
        return s
    
    # perfect hash lookup other hands
    prime_product = 1
    for card in c:
        card = card >> 16
        for i in range(13):
            if card & (1 << i):
                prime_product *= primes[i]
                break # each should only have 1 bit turned on 

    return ul.dict_unsuited_lookup[prime_product]

def eval_five_card(c:list):
    """Takes list of 5 card objects, returns the ranking of that hand"""
    bin_hand = bin_from_list(c)
    return eval_from_bin(bin_hand)

def eval_seven_card(c:list):
    """Takes list of 7 card objects, returns the ranking of the best hand"""

    # note this can be made more efficient if neccessary i just cba rn

    perms = set(itertools.permutations(c, 5))

    best_ranking = 9999 # all rankings are less than 9999
    for hand in perms:
        bin_hand = bin_from_list(hand)
        best_ranking = min(eval_from_bin(bin_hand), best_ranking)

    if best_ranking == 9999:
        return Exception

    return best_ranking
        
def bin_from_list(card_list:list):
    output = []
    for card in card_list:
        output.append(card.bin)
    return output
