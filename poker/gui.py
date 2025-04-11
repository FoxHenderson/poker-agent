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


class GUI():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Game")
        self.player1 = simple_players.Person_Player(1, "player1")
        self.computer = simple_players.Random_Player(2, "Computer")
        self.all_actions = [Action.FOLD, Action.CHECK, Action.CALL, Action.BET, Action.RAISE, Action.ALL_IN]
        self.game = Game(self.player1, self.computer)
        player_cards = self.game.players[0].cards
        self.game.pre_flop()
        self.available_actions = self.player1.valid_actions
        self.show_opponent_cards = tk.BooleanVar()  # Create a BooleanVar
        self.show_opponent_cards.set(False)
        self.refresh_page()
    
        


    
    def fold(self):
        # Handle fold action
        if self.game.to_act_index == 0:
            print("Fold button clicked!")
            self.game.fold(self.player1)
            self.refresh_page()
    def check(self):
        # Handle check action
        if self.game.to_act_index == 0:
            print("Check button")
            self.game.check(self.player1)
            self.computer.make_move(self.game)
            self.refresh_page()

            
    def bet(self):
        # Handle bet action
        if self.game.to_act_index == 0:
            print("Bet button clicked!")
            bet_amount_entry = tk.Entry(self.input_frame)
            bet_amount_entry.pack(side=tk.LEFT)
            def handle_bet():
                try:
                    bet_amount = int(bet_amount_entry.get())
                    self.game.bet(self.player1, bet_amount)
                    self.computer.make_move(self.game)                    
                    self.refresh_page()
                except :
                    print("Invalid bet amount.")

            confirm_button = tk.Button(self.input_frame, text="Confirm Bet", command=handle_bet)
            confirm_button.pack(side=tk.LEFT)
            
    def call(self):
        # Handle call action
        if self.game.to_act_index == 0:
            print("Call button clicked!")
            self.game.call(self.player1)
            self.computer.make_move(self.game)
            self.refresh_page()
            
    def raise_bet(self):
        # Handle raise action
        if self.game.to_act_index == 0:
            print("Raise button clicked!")

            raise_amount_entry = tk.Entry(self.input_frame)
            raise_amount_entry.pack(side=tk.LEFT)

            def handle_raise():
                try:
                    raise_amount = int(raise_amount_entry.get())
                    valid = self.game.raise_bet(self.player1, raise_amount)
                    print("VALID?:", valid)
                    if valid == False:
                        print("Invalid bet amount.")
                        tk.Label(self.input_frame, text="Invalid Bet amount")
                        confirm_button.pack(side=tk.LEFT)
                    else:
                        self.computer.make_move(self.game)
                        self.refresh_page()
                except ValueError:
                    print("Invalid bet amount.")
            confirm_button = tk.Button(self.input_frame, text="Confirm Raise", command=handle_raise)
            confirm_button.pack(side=tk.LEFT)


    def all_in(self):
        if self.game.to_act_index == 0:
            print("All In button clicked")
            self.game.all_in(self.player1)
            self.refresh_page()









    def card_image(self,frame, card_name):
        img = Image.open(f"img/cards/{card_name}.png")
        img = img.resize((100, 140))
        img= ImageTk.PhotoImage(img)
        return img


    def display_cards(self,frame, cards):
        card_labels = []
        for i in range(len(cards)):
            print(i)
            if cards[i] == None:
                img1 = self.card_image(frame, card_name="blank")
            else:
                img1 = self.card_image(frame, card_name=cards[i].get_img_id())
            card_labels.append(img1)
            card_1 = tk.Label(frame, image=img1)
            card_1.pack(side=tk.LEFT)

        frame.card_labels = card_labels


    def clear_page(self):
        for ele in self.root.winfo_children():
          ele.destroy()


    def refresh_page(self):           
        if self.game.previous_player == self.player1:
            self.computer.make_move(self.game)
        self.clear_page()
       
        # Player Area
        player_frame = ttk.LabelFrame(self.root, text="Your Hand")
        player_frame.pack(pady=10)

        player_cards_label = ttk.Label(player_frame, text=f"Cards:")
        player_cards_label.pack()


        player_cards = self.game.players[0].cards
        print("CARDS:",player_cards)
        self.display_cards(player_cards_label, player_cards)

        
        player_chips_label = ttk.Label(player_frame, text=f"Chips: {self.player1.stack}")
        player_chips_label.pack()

        action_frame = ttk.Frame(player_frame)
        action_frame.pack()

        self.input_frame = ttk.Frame(player_frame)
        self.input_frame.pack()


        fold_button = ttk.Button(action_frame, text="Fold", command=self.fold)
        fold_button.pack(side=tk.LEFT)
        if Action.FOLD not in self.player1.valid_actions:
            fold_button["state"] = "disabled"

        check_button = ttk.Button(action_frame, text="Check", command=self.check)
        check_button.pack(side=tk.LEFT)
        if Action.CHECK not in self.player1.valid_actions:
            check_button["state"] = "disabled"

        call_button = ttk.Button(action_frame, text="Call", command=self.call)
        call_button.pack(side=tk.LEFT)
        if Action.CALL not in self.player1.valid_actions:
            call_button["state"] = "disabled"

        bet_button = ttk.Button(action_frame, text="Bet", command=self.bet)
        bet_button.pack(side=tk.LEFT)

        if Action.BET not in self.player1.valid_actions:
            bet_button["state"] = "disabled"

        raise_button = ttk.Button(action_frame, text="Raise", command=self.raise_bet)
        raise_button.pack(side=tk.LEFT)
        if Action.RAISE not in self.player1.valid_actions:
            raise_button["state"] = "disabled"

        all_in_button = ttk.Button(action_frame, text="All In", command=self.all_in)
        all_in_button.pack(side=tk.LEFT)
        if Action.ALL_IN not in self.player1.valid_actions:
            all_in_button["state"] = "disabled"

        # Community Cards
        community_frame = ttk.LabelFrame(self.root, text=self.game.round_name)
        community_frame.pack(pady=10)

        middle_cards = self.game.board
        middle_cards.reverse()
        print(middle_cards)
        self.display_cards(community_frame, middle_cards)
        middle_cards.reverse()
        #Flop Cards


        # Pot
        pot_frame = ttk.LabelFrame(self.root, text="Pot")
        pot_frame.pack(pady=10)

        pot_label = ttk.Label(pot_frame, text=f"Pot: {self.game.pot}")
        pot_label.pack()

        # Message Log
        message_frame = ttk.LabelFrame(self.root, text="Game Log")
        message_frame.pack(pady=10)

        message_label = ttk.Label(message_frame, text=f"{self.game.game_log}")
        message_label.pack()

        # Opponents 
        self.opponents_frame = ttk.LabelFrame(self.root, text="Opponents")
        self.opponents_frame.pack(pady=10)

        opponent1_label = ttk.Label(self.opponents_frame, text=f"Computer: {self.computer.stack} chips")
        opponent1_label.pack()

        #Opponents cards

        opponent_cards_label = ttk.Label(self.opponents_frame, text=f"Cards:")
        opponent_cards_label.pack()



        checkbox_frame = ttk.Frame(self.opponents_frame)  # Frame for checkbox and label
        checkbox_frame.pack()

        checkbox = ttk.Checkbutton(checkbox_frame, text="Show Opponent Cards", variable=self.show_opponent_cards, command=self.update_opponent_cards_display)
        checkbox.pack()

        self.opponent_cards_label = ttk.Label(self.opponents_frame, text="Cards:")  # Store as instance variable
        self.opponent_cards_label.pack(side=tk.LEFT)

        self.update_opponent_cards_display()  # Initial display


    def update_opponent_cards_display(self):
        if self.show_opponent_cards.get():
            self.opponent_cards_label.destroy()
            self.opponent_cards_label = ttk.Label(self.opponents_frame, text="Cards:")
            opponent_cards = self.game.players[1].cards
            self.display_cards(self.opponent_cards_label, opponent_cards)
            self.opponent_cards_label.pack()
        else:
            # Clear the opponent cards display
            self.opponent_cards_label.destroy()
            self.opponent_cards_label = ttk.Label(self.opponents_frame, text="Cards:")
            opponent_cards = [None, None]
            self.display_cards(self.opponent_cards_label, opponent_cards)
            self.opponent_cards_label.pack()










        self.root.mainloop()

g = GUI()

