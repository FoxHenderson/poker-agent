from cmdlogic.game import Game
from cfr_player import CFR_Player
from cmdlogic.cfrgame import CFR_State
from cmdlogic.card import Card

# implementation baed on  http://modelai.gettysburg.edu/2013/cfr/cfr.pdf

class CFR_Trainer:
    def __init__(self, iterations:int=1_000_000):
        self.iterations = iterations
        
        self.info_sets = {} # maps str -> InformationSet

        self.train()


    def train(self):
        player1 = CFR_Player()
        player2 = CFR_Player()

        for iteration in range(self.iterations):
            
            # initialise game

            self.cfr(state, )
            
            if iteration % 100_000:
                print(f"Completed {iteration}/10 of training")
                print(f"Current strategy: {player1}")

def cfr(state:CFR_State, p0:float, p1:float) -> float:
    """counterfactual regret minimisation"""



    # return payoff for terminal state
