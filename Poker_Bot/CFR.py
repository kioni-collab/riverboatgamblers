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

    def traversal(self,h,p ,cards,board,t):
        if self.is_terminal(h):
            return self.util(h,p,cards,board)
        # what does a chance node do in poker, it is adding a new card to the board
        # so we have to simulate that, its actions are not fold check raise
        elif self.is_chance(h):
            # get number of cards left in deck
            # pick one randomly
            # add to board and history
            # done 
            return 
        elif self.current_player(h) == p:
            # make a regret matching function
            #
            o = self.regret_matching(h,p,cards[p],board)
            v = {}
            v_o = 0
            r = {}
            for a in self.get_actions(h):
                h_new = list(h)
                h_new.append(a)
                v[a] = self.traversal(h_new,p,cards,board,t)
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
            return self.traversal(h.append(a),p,cards,board,t)

            pass


        
        pass
    def is_terminal(self,h):
        #some unity call or game logic call
        pass
    def util(self,h,p,cards,board):
        # call to unity for money won
        pass
    def is_chance(self,h):
        # some kind of unit
        pass
    def current_player(h):
        #make a unity call or some other math for later
        pass
    def get_actions(h):
        pass
    def regret_matching():
        # firgure out what paramters to use 
        pass 