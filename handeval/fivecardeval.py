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
# can be utilised by the ai agent

def evalFromBin(c1 : int, c2 : int, c3 : int, c4 : int, c5 : int) -> np.uint16:
    q = (c1 | c2 | c3 | c4 | c5) >> 16
    s: np.int16

    # check flushes
    if (c1 & c2 & c3 & c4 & c5 & 0xf000):
        return np.uint16(ev.flushes[q])

    # check straights and high card
    s = ev.unique5[q]
    if (s):
        return np.uint16(s)
    
    # hash lookup other hands
    q = ((c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff))
    print(f"Hashed key: {q}")  
    return ev.hash_values[findFast(q)]

def findFast(u : np.uint32) -> np.uint32:
    a : np.uint32
    b : np.uint32
    r : np.uint32

    # python keeps parsing it BACK TO INT FOR NO REASON 

    u = np.uint32(u + 0xe91aaa35)
    u ^= np.uint32(u >> 16)
    u += np.uint32(u << 8)
    u ^= np.uint32(u >> 4)
    b  = np.uint32((u >> 8) & 0x1ff)
    a  = np.uint32((u + (u << 2)) >> 19)
    r  = np.uint32(a ^ ev.hash_adjust[b])
    return r

# ==================================================================
# |                     basic test cases :p                        |
# ==================================================================

# 4 kings
assert(
    evalFromBin(
        0b_00001000000000000100101100100101, # kd
        0b_00001000000000001000101100100101, # kc
        0b_00001000000000000010101100100101, # kh
        0b_00001000000000000001101100100101, # ks
        0b_00000000000010000001001100000111, # 5s
    ) == 31
)