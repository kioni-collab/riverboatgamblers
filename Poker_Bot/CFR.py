from Model import DeepCFRModel 
from Infoset import game_node
import numpy as np 
from random import choices
from torch import optim
class CFR():
    def __init__(self,players):
        self.m_v = [[] for p in range(len(players))]
        self.m_p = []
        self.value_model = DeepCFRModel()
        self.strat_model = DeepCFRModel()
        self.info_sets = {}


    # TODO 
    # figure out how to split infoset to be cards in hand, cards on board and betting postions
    # may need to change how we pass network parametrs through traversal
    # may need infoset map as well
    # find out if models are already initialized to return 0 
    def deepcfr(self,T,player,K,board:list):
        for t in range(1000):
            for p in range(len(player)):
                for k in range(K):
                    self.traversal([],p,[pl.card() for pl in player],board,self.m_v[p], self.m_p)
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
    def traversal(self,h,p ,cards,board,t,g, round):
        if self.is_terminal(h,round, len(cards) ):
            return self.util(h,p,cards,board)
        # what does a chance node do in poker, it is adding a new card to the board
        # so we have to simulate that, its actions are not fold check raise
        elif self.is_chance(g, len(cards)):
            # get number of cards left in deck
            # pick one randomly
            # add to board and history
            # done 
            g_new = []
            round += 1
            return 
        elif self.current_player(g) == p:
            # make a regret matching function
            #
            o = 0 # this will be generated from neural network
            v = {}
            v_o = 0
            r = {}
            for a in self.get_actions(g,p):
                h_new = list(h)
                h_new.append(a)
                g_new = list(g)
                g_new.append(a)
                v[a] = self.traversal(h_new,p,cards,board,t, g_new)
                v_o += o[a] * v[a]
            for a in self.get_actions(h):
                #work out what data type r(I,a) should be
                r[a] = v[a] - v_o
                pass
            self.m_v.append(([cards[p],h,board],t,r))
            return v_o 
            #insert into m_V
        else:
            # Insert the infoset and its action probabilities (I, t, σt(I)) into the strategy memory MΠ
            # edit the regret_matching stuff so it uses the right cards
            cards_not_p = list(cards).pop(p)
            o = self.regret_matching(h,p,cards_not_p,board)
            self.m_p.append(([cards[p],h,board],t,o))
            A = self.get_actions(h)
            a = choices(A,o)
            h_new = list(h)
            h_new.append(a)
            g_new = list(g)
            g_new.append(a)
            return self.traversal(h_new,p,cards,board,t, g_new)

            pass


        
        pass
    
    def is_terminal(self,h, round, player_num):
        return (round == 4) or player_num == 1
    
    def util(self,h,p,cards,board):
        # call to unity for money won
        pass
    #assume that elemts in g are like {"player_num": 3, action:"check"}
    def is_chance(self,g,player_num):
        equal_bet_list = []
        check_list = []
        for a in g:
            if a["action"] == "bet":
                check_list.clear()
                equal_bet_list.clear()
                equal_bet_list.append(a)
            if a["action"] == "call":
                equal_bet_list.append(a)
            if a["action"] == "check":
                check_list.append(a)
        return (len(equal_bet_list) == player_num) or (len(check_list) == player_num)



# we have a queue of player from 1 to n, we want tp get rid of players who already used up their turn this round
# for players we check we put them at the back of the list so the players who havent had a turn yet are at the front
#we return the first player in the queue 
#review to see if makes sense 
    def current_player(g,player_num):
        player_q = [i for i in range(player_num)]
        for l in g:
            if l["action"] != "Check":
                player_q.remove[l["player"]]
            else:
                player_q.remove[l["player"]]
                player_q.append[l["player"]]

        return player_q[0]
    
    def get_actions(g,p):
        if any([l["action"] == "bet " for l in g]):
            return ["bet","call", "fold"]
        else:
            return ["bet","check", "fold"]
        
        