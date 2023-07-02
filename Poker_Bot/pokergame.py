from pokerface import *

class poker_game:
    def __init__(self) -> None:
        pass
    
    def is_terminal(self,round, player_num, board):
        return (round == 4) or player_num == 1 or len(board) == 5
    
    def util(self,h,p,players,board,all_players):
        # call to unity for money won
        player_won = False
        if len(players) == 1:
            player_won  = True if players[0].ID() == p else False
        else:  
            try:  
                evaluator = StandardEvaluator()
                player_idx = 0
                for i in range(len(players)):
                    if p == players[i].ID():
                        player_idx = i
                print(players[player_idx].get_cards())
                curr_player = evaluator.evaluate_hand(
                tuple(players[player_idx].get_cards()), tuple(board),
                )
                other_players = [ evaluator.evaluate_hand(
                i.get_cards(), board,
                ) for i in players ]
                player_won = True if all([curr_player >= j for j in other_players]) else False
            except:
                return 0 
        all_player_idx = -1
        for i in range(len(all_players)):
            if all_players[i].ID() == p:
                all_player_idx = i
        if player_won:
             
            return sum([pl.get_bet_amt() for pl in all_players]) - all_players[all_player_idx].get_bet_amt()
        else:
            return  -all_players[all_player_idx ].get_bet_amt()

    def is_chance(self,players):
        return  all([(p.get_bet_amt() == players[0].get_bet_amt() and players[0].get_bet_amt() != 0 and p.get_last_action() is not None) for p in players]) or all([p.get_last_action() is not None and p.get_last_action() == "check" for p in players]) 


# we have a queue of player from 1 to n, we want tp get rid of players who already used up their turn this round
# for players we check we put them at the back of the list so the players who havent had a turn yet are at the front
#we return the first player in the queue 
#review to see if makes sense 
    def current_player(self,players):
        return players[0]
    
    def get_actions(self,players,round):
        if round == 1:
            return ["bet","call","fold"]
        if any([p.get_last_action() == "bet" for p in players]):
            return ["bet","call", "fold"]
        else:
            return ["bet", "check", "fold"]