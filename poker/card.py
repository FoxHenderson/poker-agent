BIN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
BIN_SUITS = [1, 2, 4, 8]

class Card:
    def __init__(self, ID):
        # ID unique integer from 1 - 52
        self.ID = ID
        self.suit = self.__Calculate_suit(ID)
        self.rank = self.__Calculate_rank(ID)
        # binary representation of the card, used for the agents internal representation of the game
        self.bin = self.__CalculateBin(ID)
        self.bin = format(self.bin, '#034b')

        # debug --------
        #print(self.suit, self.rank, self.bin)

    def __Calculate_suit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __Calculate_rank(self, ID):
        rank = {1:"Two", 2:"Three",3:"Four",4:"Five",5:"Six",6:"Seven",7:"Eight",8:"Nine",9:"Ten",10:"Jack",11:"Queen",12:"King",13: "Ace", }
        return rank[((ID - (ID%4)) / 4)+1]

    def show_card(self):
        return f"{self.rank} of {self.suit}"

    # returns card as binary number
    #+--------+--------+--------+--------+
    #|xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
    #+--------+--------+--------+--------+
    #p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
    #r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
    #cdhs = suit of card (bit turned on based on suit of card)
    #b = bit turned on depending on rank of card

    def __CalculateBin(self, ID):
        # sum maffs
        prime = BIN_PRIMES[ID // 4]
        rank = (ID // 4) << 8
        suit = (1 << (ID % 4)) << 12
        bit = (2**(ID // 4)) << 16
        return (prime | rank | suit | bit)