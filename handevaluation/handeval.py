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

    return best_ranking
        
def bin_from_list(c:list):
    output = []
    for c in list:
        output.append(c.bin)
    return output



# ==================================================================
# |                     basic test cases                           |
# ==================================================================

# flush
assert(
    eval_from_bin(
        # xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        [0b00001000_00000000_00011011_00100101, #ks
        0b00000000_00001000_00010011_00000111, #5s
        0b00000010_00000000_00011001_00011101, #Js
        0b00000100_00000000_00011010_00011111, #Qs
        0b00010000_00000000_00011100_00101001] #As
    ) == 327
)

# straight
assert(
    eval_from_bin(
        # xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        [0b00001000_00000000_00011011_00100101, #ks
        0b00000001_00000000_01001000_00010111, #10h
        0b00000010_00000000_00011001_00011101, #Js
        0b00000100_00000000_00011010_00011111, #Qs
        0b00010000_00000000_00011100_00101001] #As
    ) == 1600
)
# 4 kings
assert(
    eval_from_bin(
        #  xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        [0b00001000_00000000_01001011_00100101, # kd
         0b00001000_00000000_10001011_00100101, # kc
         0b00001000_00000000_00101011_00100101, # kh
         0b00001000_00000000_00011011_00100101, # ks
         0b00000000_00001000_00010011_00000111] # 5s
    ) == 31
)