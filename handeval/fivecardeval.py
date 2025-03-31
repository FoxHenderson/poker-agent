import evallookup as ev
import numpy as np
#from gamelogic.game import Card

# used for the hand evalutation phase of the poker game logic
#def get5cardRanking(cards : list[Card]) -> int:
#    if len(cards) != 5:
#        raise IndexError
    
#    evalFromBin(cards[0].bin, cards[1].bin, cards[2].bin, cards[3].bin, cards[4].bin)

# based on the method described at http://suffe.cool/poker/evaluator.html

# +--------+--------+--------+--------+
# |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
# +--------+--------+--------+--------+
# p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
# r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
# cdhs = suit of card (bit turned on based on suit of card)
# b = bit turned on depending on rank of card

# takes an input of binary card representations returns an integer 1-7462 representing a hands ranking, with 
# 1 being the best hand type (all royal flushes) 
# and 7462 being the worst (75432o)

def evalFromBin(c1 : int, c2 : int, c3 : int, c4 : int, c5 : int):

    q = (c1 | c2 | c3 | c4 | c5)
    q = q >> 16

    # check if hand is a flush
    # check flushes
    if (c1 & c2 & c3 & c4 & c5 & 0xF000):
        return ev.flushes[q]
    
    # check straights and high card
    s = ev.unique5[q]
    if (s):
        return s
    
    # hash lookup other hands
    q = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff)
    print(find_fast(q))
    return ev.hash_values[find_fast(q)]

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
        0b00001000_00000000_00011011_00100101, #ks
        0b00000000_00001000_00010011_00000111, #5s
        0b00000010_00000000_00011001_00011101, #Js
        0b00000100_00000000_00011010_00011111, #Qs
        0b00010000_00000000_00011100_00101001 #As
    ) == 327
)

# straight
assert(
    evalFromBin(
        # xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        0b00001000_00000000_00011011_00100101, #ks
        0b00000001_00000000_01001000_00010111, #10h
        0b00000010_00000000_00011001_00011101, #Js
        0b00000100_00000000_00011010_00011111, #Qs
        0b00010000_00000000_00011100_00101001 #As
    ) == 1600
)
# 4 kings
assert(
    evalFromBin(
        # xxxAKQJT 98765432 CDHSrrrr xxPPPPPP
        0b00001000_00000000_01001011_00100101, # kd
        0b00001000_00000000_10001011_00100101, # kc
        0b00001000_00000000_00101011_00100101, # kh
        0b00001000_00000000_00011011_00100101, # ks
        0b00000000_00001000_00010011_00000111 # 5s
    ) == 31
)