import evallookup as ev
import unsuited_lookup as ul
import numpy as np
#from gamelogic.game import Card

# used for the hand evalutation phase of the poker game logic
#def get5cardRanking(cards : list[Card]) -> int:
#    if len(cards) != 5:
#        raise IndexError
    
#    evalFromBin(cards[0].bin, cards[1].bin, cards[2].bin, cards[3].bin, cards[4].bin)

def evalFromBin(c:list):
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

def find_fast(u):
    u = (u+0xe91aaa35) & 0xFFFFFFFF
    u ^= u >> 16
    u = (u+(u << 8)) & 0xFFFFFFFF
    u ^= u >> 4
    b  = (u >> 8) & 0x1ff
    a  = (u + (u << 2)) >> 19
    # & 0xFFFF because python
    r  = (a ^ ev.hash_adjust[b]) & 0xFFFF
    return r;

# ==================================================================
# |                     basic test cases                           |
# ==================================================================

# flush
assert(
    evalFromBin(
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
    evalFromBin(
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
    evalFromBin(
        #  xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        [0b00001000_00000000_01001011_00100101, # kd
         0b00001000_00000000_10001011_00100101, # kc
         0b00001000_00000000_00101011_00100101, # kh
         0b00001000_00000000_00011011_00100101, # ks
         0b00000000_00001000_00010011_00000111] # 5s
    ) == 31
)