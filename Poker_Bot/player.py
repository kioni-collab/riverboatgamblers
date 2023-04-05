class Player():
    def __init__(self,id,cards) -> None:
        self.id = id
        self.cards = cards
        self.last_action = None
        self.bet_amt = 0
        self.bets_this_round  = 0
    def set_bet_amt(self,amt):
        self.bet_amt = amt
    def incri_bet(self,amt):
        self.bet_amt += amt
    def get_bet_amt(self):
        return self.bet_amt
    def set_last_action(self,action):
        self.last_action = action
    def get_last_action(self):
        return self.last_action
    def get_cards(self):
        return self.cards
    def ID(self):
        return self.id
    

