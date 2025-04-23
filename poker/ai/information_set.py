import numpy as np
import jsonpickle

from cmdlogic.cfrgame import CFR_State
from cmdlogic.card import Card
from cmdlogic.evaluation.handeval import eval_seven_card
from cmdlogic.deck import Deck

# abstracted actions
class AbstractActions:
    CHECK_FOLD = 0
    CALL = 1
    BET_HALF = 2 # bet half pot
    BET_POT = 3
    ALL_IN = 4

    NUM_ACTIONS = 5

class InformationSet():
    """
    Important to note that the information set should only contain information that is visible to the player
    """
    def __init__(self, state:CFR_State):
        """
            key will contain the (unique) string representation of the game state in the following format. 
            Card bucket (integer 1-5)
            Board (Integer ID , XX to signify a card hasn't been dealt yet)
                - Maybe board needs to be 
            Action history (Need to figure out some character rep of the abstracted actions)
        """

        self.regret_sum = [0.0] * AbstractActions.NUM_ACTIONS
        self.strategy = [0.0] * AbstractActions.NUM_ACTIONS
        self.strategy_sum = [0.0] * AbstractActions.NUM_ACTIONS

        # number of legal actions for the player in the current state
        self.NUM_LEGAL_ACTIONS = state.player.get_actions()

    # this needs to filter out legal actions to probability 0
    def get_strategy(self, realization_weight: float) -> list:
        """
        Get the current mixed strategy using regret matching.

        realization_weight is the probability of us actually getting the position we are in
        (forgive the american spelling - I want to remain consistent naming conventions with the paper)
        """
        positive_regrets = [max(r, 0.0) for r in self.regret_sum]
        normalizing_sum = sum(positive_regrets)
        for a in range(AbstractActions.NUM_ACTIONS):
            if normalizing_sum > 0:
                self.strategy[a] = positive_regrets[a] / normalizing_sum
            else:
                self.strategy[a] = 1.0 / AbstractActions.NUM_ACTIONS  
            self.strategy_sum[a] += realization_weight * self.strategy[a]
        return self.strategy
        
    def getAverageStrategy(self) -> list:
        """
        Get average information set mixed strategy across all training iterations
        """
        avg_strategy = [0.0] * self.NUM_LEGAL_ACTIONS
        normalising_sum = 0

        for a in range(self.NUM_LEGAL_ACTIONS):
            normalising_sum += self.strategy_sum[a]
        for a in range(self.NUM_LEGAL_ACTIONS):
            if normalising_sum > 0:
                avg_strategy[a] = self.strategy_sum[a] / normalising_sum
            else:
                avg_strategy[a] = 1 / self.NUM_LEGAL_ACTIONS

        return avg_strategy
    
    @staticmethod
    def get_key_from_state(state:CFR_State) -> str:
        """
        Calculates the current key based on the game state (our game implementation wrapper)
        Currently takes:
            - Hand bucket (int 1-5)
            - Board (IDK how to abstract this )
            - Action history (see history method for defns)
        and is of the form "bucket;board;history"
        """
        # this will need to change when state has been implemented
        hole_cards = state.get_hole_cards()
        board = state.get_board()
        history = state.get_history()

        hs2 = InformationSet.calculate_hs2(hole_cards, board)
        bucket = InformationSet.bucket_from_hs2(hs2)

        board_str = ''.join([str(card.id for card in board)]) if board else ""
        action_str = InformationSet.encode_action_history(history)

        return f"{bucket};{board_str};{action_str}"
    
    @staticmethod
    def calculate_hs2(hole_cards:list[Card], board:list[Card]=None, iterations=500) -> float:
        test_deck = Deck()

        # remove KNOWN dealt cards from deck
        for card in hole_cards + board:
            test_deck.deck.remove(card)

        hs_sum = 0

        for i in range(iterations):
            test_deck.shuffle_deck()

            # generate random opponent hand
            villain_hand = [test_deck.peek[-1], test_deck.peek[-2]]

            cards_to_deal = 5 - len(board)
            board_extension = []

            for j in range(cards_to_deal):
                board_extension.append(test_deck.peek[j])
            
            hero_score = eval_seven_card(hole_cards + board + board_extension)
            villain_score = eval_seven_card(villain_hand + board + board_extension)

            # villain wins
            if hero_score > villain_score:
                hs = 0
            elif hero_score == villain_score: # tie
                hs = 0.5
            else: # hero wins
                hs = 1
            
            hs_sum += hs ** 2
        
        return hs_sum / iterations

    # this may be too many buckets
    @staticmethod
    def bucket_from_hs2(hs2:float) -> int:
        if hs2 < 0.2:
            return 1
        elif hs2 < 0.4:
            return 2
        elif hs2 < 0.6:
            return 3
        elif hs2 < 0.8:
            return 4
        else:
            return 5
        
    @staticmethod
    def encode_action_history(history) -> str:
        """
        Convert action history into string format
        """
        action_map = {
            AbstractActions.CHECK_FOLD: 'F',
            AbstractActions.CALL: 'C',
            AbstractActions.BET_HALF: 'H',
            AbstractActions.BET_POT: 'P',
            AbstractActions.ALL_IN: 'A'
        }
        return ''.join(action_map.get(action, '?') for action in history)