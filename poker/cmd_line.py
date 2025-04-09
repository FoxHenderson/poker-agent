class cmd_line:
    def __init__(self):
        self.player1 = simple_players.Person_Player(1, "player1")
        self.player2 = simple_players.Random_Player(2, "Computer")
        self.available_actions = [Action.FOLD, Action.CHECK, Action.CALL, Action.BET, Action.RAISE, Action.ALL_IN]
        self.game = Game(self.player1, self.player2)
        player_cards = self.game.players[0].cards
        self.refresh_page()


    
    def fold(self):
        # Handle fold action
        if game.to_act_index == 0:
            print("Fold button clicked!")
            self.game.fold(self.player1)
            self.valid_actions_for_opponent = self.player1.get_available_actions((Action.FOLD, 0))
            self.refresh_page()
    def check(self):
        # Handle check action
        if game.to_act_index == 0:
            print("Check button")
            self.game.check(self.player1)
            self.available_actions = self.player1.get_available_actions((Action.CHECK, 0))
            self.refresh_page()
    def bet(self):
        # Handle bet action
        if game.to_act_index == 0:
            print("Bet button clicked!")
            bet_amount_entry = tk.Entry(self.root) # Entry widget for bet amount
            bet_amount_entry.pack(side=tk.LEFT)
            self.available_actions = self.player1.get_available_actions((Action.BET, 0))
            self.refresh_page()
    def call(self):
        # Handle call action
        if game.to_act_index == 0:
            print("Call button clicked!")
            self.game.call(self.player1)
            self.available_actions = self.player1.get_available_actions((Action.CALL, 0))
            self.refresh_page()
    def raise_bet(self):
        # Handle raise action
        if game.to_act_index == 0:
            print("Raise button clicked!")
            action = self.game.raise_bet(self.player1)
            self.available_actions = self.player1.get_available_actions((Action.RAISE, 0))
            self.refresh_page()
    def all_in(self):
        if game.to_act_index == 0:
            print("All In button clicked")
            self.game.all_in(self.player1)
            self.available_actions = self.player1.get_available_actions((Action.ALL_IN, 0))
            self.refresh_page()




    
    def refresh_page(self):
        
        
