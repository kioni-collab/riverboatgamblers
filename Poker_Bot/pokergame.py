from pokerface import *

class poker_game:
    def __init__(self) -> None:
        pass
    
    def is_terminal(self,round, player_num):
        return (round == 4) or player_num == 1
    
    def util(self,h,p,cards,board):
        # call to unity for money won
        pass
    #assume that elemts in g are like {"player_num": 3, action:"check"}

    def is_chance(self,players,round):
        return  all([(p.get_bet_amt() == players[0].get_bet_amt() and players[0].get_bet_amt() != 0 and p.get_last_action() is not None) for p in players]) or all([p.get_last_action() is not None and p.last_action() == "check" for p in players]) or round==0


# we have a queue of player from 1 to n, we want tp get rid of players who already used up their turn this round
# for players we check we put them at the back of the list so the players who havent had a turn yet are at the front
#we return the first player in the queue 
#review to see if makes sense 
    def current_player(players):
        return players[0]
    
    def get_actions(players,round):
        if round == 1:
            return ["bet","fold"]
        if any([p.get_last_action() == "bet" for p in players]):
            return ["bet","call", "fold"]
        else:
            return ["bet", "check", "fold"]