BIN_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
BIN_SUITS = [1, 2, 4, 8]

class Card:
    # returns card as binary number
    #+--------+--------+--------+--------+
    #|xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
    #+--------+--------+--------+--------+
    #p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
    #r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
    #cdhs = suit of card (bit turned on based on suit of card)
    #b = bit turned on depending on rank of card

    def __init__(self, ID):
        # ID unique integer from 1 - 52
        self.ID = ID
        self.suit = self.__Calculate_suit(ID)
        self.rank = self.__Calculate_rank(ID)
        # binary representation of the card, used for the agents internal representation of the game
        self.bin = int(self.__CalculateBin(ID))

        # debug --------
        #print(self.suit, self.rank, self.bin)

    def __Calculate_suit(self, ID):
        suits = {0:"Clubs", 1: "Diamonds", 2: "Hearts",3:"Spades"}
        return suits[ID % 4]

    def __Calculate_rank(self, ID):
        rank = {1:"2", 2:"3",3:"4",4:"5",5:"6",6:"7",7:"8",8:"9",9:"10",10:"Jack",11:"Queen",12:"King",13: "Ace", }
        return rank[((ID - (ID%4)) / 4)+1]

    def show_card(self):
        return f"{self.rank} of {self.suit}"
    
    def __str__(self):
        return self.show_card()
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
        # return f"{self.rank} of {self.suit} : {self.bin}"
    
    def get_img_id(self):
        return self.rank.lower() + "_" + "of" + "_" + self.suit.lower()

    def __CalculateBin(self, ID):
        # sum maffs
        prime = BIN_PRIMES[ID // 4]
        rank = (ID // 4) << 8
        suit = (1 << (ID % 4)) << 12
        bit = (2**(ID // 4)) << 16
        return (prime | rank | suit | bit)
