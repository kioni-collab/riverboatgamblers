from pokerface import *

class poker_game:
    def __init__(self, player_banks) -> None:
        self.game  = NoLimitTexasHoldEm(Stakes(),player_banks)
        self.nature = self.game.nature
    
    def deal_board(self, card_num):
        for i in range(card_num):
            self.nature.deal_board()
    def deal_cards(self,player_num):
        for i in range(player_num * 2):
            self.nature.deal_hole()

    # we should build a list of moves the player can do
    # the list will be function that the player will pick 1 from to call
    # i hope works like this 
    # https://stackoverflow.com/questions/5461571/call-list-of-function-using-list-comprehension
    def player_moves(self,player):
        moves = []
        if self.game.players[player].can_fold():
            moves.append(self.game.players[player].fold)
        elif self.game.players[player].can_check_call():
            moves.append(self.game.players[player].check_call())
    
    # resolves winner and disgrubtes pot, we want to see that was the winnings/losings for our player
    def winner(self, player):
        prev_amount  = self.game.players[player].stack
        for p in self.game.players:
            p.showdown()
        return self.game.players[player].stack - prev_amount
    
    # to see if we are at a chance node then all players must not be able do do any moves
    # so make a functi
    #

#assume that elemts in h are like {"player_num": p3, action:"checl"}
def is_chance(g,player_num):
    checked = []
    non_check_actions = 0
    for l in g:
        if l["action"] == "Check":
            if l not in checked:
                checked.append(l)
            else:
                checked.remove(l)
        else:
            non_check_actions += 1
    
    if non_check_actions % player_num == 0 and (len(checked) == 0 or len(checked)==player_num):
        return True
    return False