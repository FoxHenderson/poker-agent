import tkinter as tk
from tkinter import ttk
#from game import Gui_Game as game
from PIL import ImageTk, Image



def fold():
    # Handle fold action
    print("Fold button clicked!")

def check():
    # Handle check action
    print("Check button")
def bet():
    # Handle bet action
    print("Bet button clicked!")

def call():
    # Handle call action
    print("Call button clicked!")



def raise_bet():
    # Handle raise action
    print("Raise button clicked!")


def card_image(frame, card_name):
    img = Image.open(f"img/cards/{card_name}.png")
    img = img.resize((50, 70))
    img= ImageTk.PhotoImage(img)
    return img


def display_cards(frame, cards):
    card_labels = []
    for i in range(len(cards)):
        #img1 = card_image(frame, card_name=card_img_id(cards[0]))
        img1 = card_image(frame, card_name=cards[i])
        card_labels.append(img1)
        card_1 = tk.Label(frame, image=img1)
        card_1.pack(side=tk.LEFT)

    frame.card_labels = card_labels







def main():
    root = tk.Tk()
    root.title("Poker Game")

    # Player Area
    player_frame = ttk.LabelFrame(root, text="Your Hand")
    player_frame.pack(pady=10)

    player_cards_label = ttk.Label(player_frame, text=f"Cards:")
    player_cards_label.pack()


   # player_cards = game.players[0].cards
    player_cards = ["2_of_spades", "queen_of_hearts"]
    display_cards(player_cards_label, player_cards)

    
    player_chips_label = ttk.Label(player_frame, text="Chips: 1000")
    player_chips_label.pack()

    action_frame = ttk.Frame(player_frame)
    action_frame.pack()

    fold_button = ttk.Button(action_frame, text="Fold", command=fold)
    fold_button.pack(side=tk.LEFT)

    check_button = ttk.Button(action_frame, text="Check", command=check)
    fold_button.pack(side=tk.LEFT)

    call_button = ttk.Button(action_frame, text="Call", command=call)
    call_button.pack(side=tk.LEFT)

    bet_button = ttk.Button(action_frame, text="Bet", command=bet)
    bet_button.pack(side=tk.LEFT)

    raise_button = ttk.Button(action_frame, text="Raise", command=raise_bet)
    raise_button.pack(side=tk.LEFT)

    all_in_button = ttk.Button(action_frame, text="All In", command=raise_bet)
    all_in_button.pack(side=tk.LEFT)

    # Community Cards
    community_frame = ttk.LabelFrame(root, text="Community Cards")
    community_frame.pack(pady=10)

    middle_cards = ["jack_of_spades", "4_of_clubs", "3_of_clubs"]
    display_cards(community_frame, middle_cards)
    #Flop Cards
    


    
    community_cards_label.pack()

    # Pot
    pot_frame = ttk.LabelFrame(root, text="Pot")
    pot_frame.pack(pady=10)

    pot_label = ttk.Label(pot_frame, text="Pot: 50")
    pot_label.pack()

    # Message Log
    message_frame = ttk.LabelFrame(root, text="Game Log")
    message_frame.pack(pady=10)

    message_label = ttk.Label(message_frame, text="Welcome to the poker game!")
    message_label.pack()

    # Opponents (Simplified)
    opponents_frame = ttk.LabelFrame(root, text="Opponents")
    opponents_frame.pack(pady=10)

    opponent1_label = ttk.Label(opponents_frame, text="Opponent 1: 800 chips")
    opponent1_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
