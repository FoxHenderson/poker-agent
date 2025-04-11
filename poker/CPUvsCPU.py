import tkinter as tk
from tkinter import ttk
#from game import Gui_Game as game
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
from game_no_loop import Game
from PIL import ImageTk, Image
import simple_players
from actions import Action


class CPUvsCPU():
    def __init__(self):
        self.player1 = simple_players.Simple_CFR_Player(1, "player1")
        self.player2 = simple_players.Simple_CFR_Player(2, "player2")
        self.all_actions = [Action.FOLD, Action.CHECK, Action.CALL, Action.BET, Action.RAISE, Action.ALL_IN]
        self.game = Game(self.player1, self.player2)
        self.game.pre_flop()
        self.available_actions = self.player1.valid_actions
        self.main_loop()
    
    def main_loop(self):
        while self.game.winner == False:
            self.player1.make_move(self.game)
            print("PLAYER 1:", self.player1.get_player_game_stats(self.game))
            if self.game.winner ==False:
                self.player2.make_move(self.game)
                print("PLAYER 2:", self.player2.get_player_game_stats(self.game))
        print("GAMELOG: \n\n", self.game.game_log)

        print(self.game.winner, "Wins")
g = CPUvsCPU()

