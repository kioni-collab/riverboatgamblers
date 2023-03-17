from Model import DeepCFRModel 
import numpy as np 
from random import choices
import random
from torch import optim
from player import Player
import torch
class CFR():
    def __init__(self,players):
        self.m_v = [[] for p in range(len(players))]
        self.m_p = []
        #self.value_model = DeepCFRModel()
        #self.strat_model = DeepCFRModel()
        self.info_sets = {}


    # TODO 
    # figure out how to split infoset to be cards in hand, cards on board and betting postions
    # may need to change how we pass network parametrs through traversal
    # may need infoset map as well
    # find out if models are already initialized to return 0 
    def deepcfr(self,T,players,K,board:list):

        for t in range(1000):
            for p in range(len(players)):
                for k in range(K):

                    self.traversal([],p,players,board, 10,20,0)
                # train model 
                self.value_model = DeepCFRModel()
                optimizer = optim.Adam(self.value_model.parameters())
                target_regret = np.asarray([r[2] for r in self.m_p])
                info_set = [r[0] for r in self.m_p] # split up between card,board and bet
                player_cards = [i[0] for i in info_set]
                board_cards = [i[1] for i in info_set]
                cards = np.array([np.array(xi) for xi in [player_cards,board_cards]])# hopfully this is good
                histories = [i[2] for i in info_set]
                bets = np.array([True if i == "b" else False for i in histories ]) # this may not be the right format
                t_val = np.asarray([r[1] for r in self.m_p])
                for e in range(100):
                    optimizer.zero_grad()
                    pred = self.value_model(cards,bets) # switch out when not exhuasted
                    loss = self.value_model.loss(pred,target_regret,t_val)
                    loss.backwards()
                    optimizer.step()
        self.strat_model = DeepCFRModel()
        optimizer = optim.Adam(self.strat_model.parameters())
        target_strategy = np.asarray([r[2] for r in self.m_v])
        info_set = [r[0] for r in self.m_v] # split up between card,board and bet
        player_cards = [i[0] for i in info_set]
        board_cards = [i[1] for i in info_set]
        cards = np.array([np.array(xi) for xi in [player_cards,board_cards]]) # hopfully this is good
        histories = [i[2] for i in info_set]
        bets = np.array([True if i == "b" else False for i in histories ]) # this may not be the right format
        t_val = np.asarray([r[1] for r in self.m_v])
        for e in range(100):
            optimizer.zero_grad()
            pred = self.strat_model(cards,bets) # switch out when not exhuasted
            loss = self.strat_model.loss(pred,target_strategy,t_val)
            loss.backwards()
            optimizer.step()
        pass            

# g is actions i that round
    def traversal(self,h,p ,players,board,t,cur_bet, min_bet,max_bet,round,deck):
        if self.is_terminal(round, len(players) ):
            return self.util(h,p,players,board)
        # what does a chance node do in poker, it is adding a new card to the board
        elif self.is_chance(players,round):
            # get number of cards left in deck
            # pick one randomly
            # add to board and history
            # done 
            board.append(deck.pop(random.randrange(len(deck))))
            h.append("board_card")
            #reset all player actions to none
            new_players = list(players)
            for pl in new_players:
                pl.set_last_action(None) 

            round += 1
            return self.traversal(h,p ,new_players,board,t,cur_bet, min_bet,max_bet,round,deck) 
        
        elif self.current_player(players).ID() == p:
            # make a regret matching function
            #
            o = 0 # this will be generated from neural network
            v = {}
            v_o = 0
            r = {}
            for a in self.get_actions(players,round):
                h_new = list(h)
                h_new.append(a)
                new_players = list(players)
                new_players[0].set_last_action(a)
                if a == "bet":
                    if round < 3:
                        cur_bet += min_bet
                    else:
                        cur_bet += max_bet
                    new_players[0].set_bet_amt(cur_bet)
                elif a == "call":
                    new_players[0].set_bet_amt(cur_bet)
                
                if a == "fold":
                    new_players = new_players[1:]
                else:
                    new_players = new_players[1:] + new_players[0]

                v[a] = self.traversal(h_new,p,new_players,board,t,cur_bet, min_bet, max_bet, round)
                v_o += o[a] * v[a]
            for a in self.get_actions(h):
                #work out what data type r(I,a) should be
                r[a] = v[a] - v_o
                pass
            self.m_v.append(([players[p].get_cards(),h,board],t,r))
            return v_o 
            #insert into m_V
        else:
            # Insert the infoset and its action probabilities (I, t, σt(I)) into the strategy memory MΠ
            # edit the regret_matching stuff so it uses the right cards
            o = None # add neural network
            self.m_p.append(([players[0].get_cards(),h,board],t,o))
            A = self.get_actions(h)
            a = choices(A,o)
            h_new = list(h)
            h_new.append(a)
            new_players = list(players)
            new_players[0].set_last_action(a)
            if a == "bet":
                if round < 3:
                    cur_bet += min_bet
                else:
                    cur_bet += max_bet
                new_players[0].set_bet_amt(cur_bet)
            elif a == "call":
                new_players[0].set_bet_amt(cur_bet)
            
            if a == "fold":
                new_players = new_players[1:]
            else:
                new_players = new_players[1:] + new_players[0]
                
            return self.traversal(h_new,p,new_players,board,t,cur_bet, min_bet,max_bet,round)

            pass


        
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

players = [Player(1, []),Player(2,[]), Player(3,[])]

print(CFR(players).is_chance(players,0))
hole = [[1,2]]
print(torch.tensor(hole).shape)
board = [[3, 4,5,6]]
turn = [[7]]
cards = ( torch.tensor(hole),torch.tensor(board), [torch.tensor(turn)])
#mase sure there is enough buffering/padding for bets 
bets = [[0,-1,0,-1,-1, 0, 0,0,0,0]]
print(DeepCFRModel(2,10,4).forward(cards,torch.tensor(bets) ))
bets = [[0,-1,0,-1,-1]]
print(DeepCFRModel(2,5,4).forward(cards,torch.tensor(bets) ))