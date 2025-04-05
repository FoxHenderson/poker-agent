from game import CL_Game
from simple_players import Command_Line_Player, Random_Player

while True:
    user = Command_Line_Player(0, "JWM")
    cpu = Random_Player(1, "cpu1")
    game = CL_Game(user, cpu)
    game.game_loop()