import tkinter as tk
from tkinter import ttk
#from game import Gui_Game as game
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
#from game import Gui_Game as game
from PIL import ImageTk, Image
import simple_players
from actions import Action


class gui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Game")
        self.player1 = simple_players.Person_Player(1, "player1")
        self.available_actions = [Action.FOLD, Action.CHECK, Action.CALL, Action.BET, Action.RAISE, Action.ALL_IN]

    def clear_page(self):
        for ele in self.root.winfo_children():
          ele.destroy()

    
    def fold(self):
        # Handle fold action
        print("Fold button clicked!")
        self.available_actions = self.player1.get_available_actions((Action.FOLD, 0))
        self.clear_page()
        self.main()
    def check(self):
        # Handle check action
        print("Check button")
        self.available_actions = self.player1.get_available_actions((Action.CHECK, 0))
        self.clear_page()
        self.main()
    def bet(self):
        # Handle bet action
        print("Bet button clicked!")
        bet_amount_entry = tk.Entry(self.root) # Entry widget for bet amount
        bet_amount_entry.pack(side=tk.LEFT)
        self.available_actions = self.player1.get_available_actions((Action.BET, 0))
        self.clear_page()
        self.main()
    def call(self):
        # Handle call action
        print("Call button clicked!")
        self.available_actions = self.player1.get_available_actions((Action.CALL, 0))
        self.clear_page()
        self.main()
    def raise_bet(self):
        # Handle raise action
        print("Raise button clicked!")
        self.available_actions = self.player1.get_available_actions((Action.RAISE, 0))
        self.clear_page()
        self.main()
    def all_in(self):
        print("All In button clicked")
        self.available_actions = self.player1.get_available_actions((Action.ALL_IN, 0))
        self.clear_page()
        self.main()

    def card_image(self,frame, card_name):
        img = Image.open(f"img/cards/{card_name}.png")
        img = img.resize((50, 70))
        img= ImageTk.PhotoImage(img)
        return img


    def display_cards(self,frame, cards):
        card_labels = []
        for i in range(len(cards)):
            print(i)
            if cards[i] == None:
                img1 = self.card_image(frame, card_name="blank")
            else:
                #img1 = card_image(frame, card_name=card_img_id(cards[0]))
                img1 = self.card_image(frame, card_name=cards[i])
            card_labels.append(img1)
            card_1 = tk.Label(frame, image=img1)
            card_1.pack(side=tk.LEFT)

        frame.card_labels = card_labels







    def main(self):


        # Player Area
        player_frame = ttk.LabelFrame(self.root, text="Your Hand")
        player_frame.pack(pady=10)

        player_cards_label = ttk.Label(player_frame, text=f"Cards:")
        player_cards_label.pack()


       # player_cards = game.players[0].cards
        player_cards = ["2_of_spades", "queen_of_hearts"]
        self.display_cards(player_cards_label, player_cards)

        
        player_chips_label = ttk.Label(player_frame, text="Chips: 1000")
        player_chips_label.pack()

        action_frame = ttk.Frame(player_frame)
        action_frame.pack()


        fold_button = ttk.Button(action_frame, text="Fold", command=self.fold)
        fold_button.pack(side=tk.LEFT)
        if Action.FOLD not in self.available_actions:
            fold_button["state"] = "disabled"

        check_button = ttk.Button(action_frame, text="Check", command=self.check)
        check_button.pack(side=tk.LEFT)
        if Action.CHECK not in self.available_actions:
            check_button["state"] = "disabled"

        call_button = ttk.Button(action_frame, text="Call", command=self.call)
        call_button.pack(side=tk.LEFT)
        if Action.CALL not in self.available_actions:
            call_button["state"] = "disabled"

        bet_button = ttk.Button(action_frame, text="Bet", command=self.bet)
        bet_button.pack(side=tk.LEFT)

        if Action.BET not in self.available_actions:
            bet_button["state"] = "disabled"

        raise_button = ttk.Button(action_frame, text="Raise", command=self.raise_bet)
        raise_button.pack(side=tk.LEFT)
        if Action.RAISE not in self.available_actions:
            raise_button["state"] = "disabled"

        all_in_button = ttk.Button(action_frame, text="All In", command=self.all_in)
        all_in_button.pack(side=tk.LEFT)
        if Action.ALL_IN not in self.available_actions:
            all_in_button["state"] = "disabled"

        # Community Cards
        community_frame = ttk.LabelFrame(self.root, text="Community Cards")
        community_frame.pack(pady=10)

        middle_cards = ["jack_of_spades", "4_of_clubs", "3_of_clubs", None, None]
        self.display_cards(community_frame, middle_cards)
        #Flop Cards
        


        

        # Pot
        pot_frame = ttk.LabelFrame(self.root, text="Pot")
        pot_frame.pack(pady=10)

        pot_label = ttk.Label(pot_frame, text="Pot: 50")
        pot_label.pack()

        # Message Log
        message_frame = ttk.LabelFrame(self.root, text="Game Log")
        message_frame.pack(pady=10)

        message_label = ttk.Label(message_frame, text="Welcome to the poker game!")
        message_label.pack()

        # Opponents (Simplified)
        opponents_frame = ttk.LabelFrame(self.root, text="Opponents")
        opponents_frame.pack(pady=10)

        opponent1_label = ttk.Label(opponents_frame, text="Opponent 1: 800 chips")
        opponent1_label.pack()

        self.root.mainloop()

g = gui()
g.main()

