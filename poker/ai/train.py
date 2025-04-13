from cmdlogic.game import Game
from cfr_player import CFR_Player
from cmdlogic.card import Card

# implementation baed on  http://modelai.gettysburg.edu/2013/cfr/cfr.pdf

class CFR_Trainer:
    def __init__(self, iterations):
        self.iterations = iterations
        
        self.node_map = {}

        self.train()


    def train(self):
        iterations = 1_000_000

        player1 = CFR_Player()
        player2 = CFR_Player()

        for iteration in range(iterations):
            training_game = Game(player1, player2)


            if iteration % 100_000:
                print(f"Completed {iteration}/10 of training")
                print(f"Current strategy: {player1.}")

def cfr(game:Game, history:list, player1:CFR_Player, player2:CFR_Player) -> float:
    """counterfactual regret minimisation"""



    # return payoff for terminal state
    if 