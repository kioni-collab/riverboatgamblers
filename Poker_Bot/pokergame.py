from pokerface import *

class poker_game:
    def __init__(self) -> None:
        pass
    
    def is_terminal(self,round, player_num):
        return (round == 4) or player_num == 1
    
    def util(self,h,p,players,board):
        # call to unity for money won
        evaluator = StandardEvaluator()
        curr_player = evaluator.evaluate_hand(
        parse_cards(players[p].get_cards()), parse_cards(board),
        )
        other_players = [ evaluator.evaluate_hand(
        parse_cards(players[i].get_cards()), parse_cards(board),
        ) for i in players ]
        top_score = True if all([curr_player >= j for j in other_players]) else False

        if top_score:
             
            return sum([pl.get_bet_amt() for pl in players]) - players[p].get_bet_amt()
        else:
            return  -players[p].get_bet_amt()

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