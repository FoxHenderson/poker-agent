from enum import Enum
from cmdlogic.game import Game


class CFR_State:
    
    def __init__(self,
                 game: Game,
                 player_id: int):
        self.game = game
        self.current_round = game.round_index
        self.player_id = player_id
        self.player = game.players[player_id]
        self.player_hand = self.player.cards
        self.board_cards = [x for x in game.board if x is not None]
        self.action_history = game.action_history
        self.pot = game.pot



    def calculate_hand_strength_squared(self, iterations, num_of_buckets):

        test_deck = Deck()
        print("CALCULATING HAND STRENGTH")

        # Remove KNOWN dealt cards from the deck
        for card in self.player_hand + self.board_cards:
            test_deck.remove(card)

        hero_hs_sum = ()

        for i in range(iterations):
            test_deck.shuffle_deck()

            #Generate random opponent hand
            villain_hand = [test_deck.peek[-1], test_deck.peek[-2]]

            cards_to_deal = 5 - len(board)
            board_extension = []

            for j in range(cards_to_deal):
                board_extension.append(test.deck.peek(j))

            hero_score = eval_seven_card(self.player_hand + self.board_cards + board_extension)
            villain_score = eval_seven_card(villain_hand + self.board_cards + board_extension)

            if hero_score > villain_score:
                hero_hs = 0
                villain_hs = 1
            elif hero_score == villain_score:
                hero_hs = 0.5
                villain_hs = 0.5
            else:
                hero_hs = 1
                villain_hs = 0

            hero_hs_sum += hero_hs**2
            villain_hs_sum += villain_hs**2
        # Since the results are scewed, they cannot be inversely compared
        return bucket(hero_hs_sum / iterations, num_of_buckets)


            

    def bucket(self, hs2: float, num_of_buckets: int) -> int:
        return min(int((hs2 * num_of_buckets )// 1), num_of_buckets)
        

    # I THINK WE ALSO NEED A METRIC WHICH THINKS ABOUT HOW CONFIDENT AN OPPOSITION PLAYER IS GOING TO FEEL 

    def get_possible_actions(self):
        player_to_act = self.game.players[self.game.to_act_index]
        last_action = player_to_act.get_last_action(self.current_round)
        print(player_to_act, last_action)
        return player_to_act.get_available_actions(last_action)

    def get_hole_cards(self):
        return self.player_hands

    def get_board(self):
        return self.board_cards

    def get_history(self):
        return self.action_history

    def get_hs2(self):
        return self.calculate_hs2(iterations=500, num_of_buckets=5)

    def get_pot(self):
        return self.pot

    def is_terminal(self):
        print("IS IT TERMINAL?:", self.game.ended)
        return self.game.ended


