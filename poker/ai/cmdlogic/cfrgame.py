from .player import Player
from .game import Game
from cfr_player import AbstractActions

class CFR_State:
    def __init__(
            self, 
            game:Game, 
            player_id: int, 
            history:dict,

        ):

        self.game = game
        self.current_player = game.players[current_player]
        self.terminal = False
        self.winner = None
        self.history = history

        def is_terminal(self):
            return game.game_state == 4 or any(player.folded for player in self.game.players)
        
        def apply_action(action:AbstractActions) -> CFR_State:
            return NotImplementedError
