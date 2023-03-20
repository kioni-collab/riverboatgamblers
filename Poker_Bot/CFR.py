from Model import DeepCFRModel 
import numpy as np 
from random import choices
import random
from torch import optim
from player import Player
import torch
from pokergame import poker_game
from pokerface import *

BET_PADDING = 100
CARD_TYPES = 2
NACTIONS = 3
class CFR():
    def __init__(self,players):
        self.m_v = [[] for p in range(len(players))]
        self.m_p = []
        self.value_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
        self.strat_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
        self.card_to_label = self.card_to_label(StandardDeck())


    # TODO 
    # figure out how to split infoset to be cards in hand, cards on board and betting postions
    # may need to change how we pass network parametrs through traversal
    # may need infoset map as well
    # find out if models are already initialized to return 0 
    def deepcfr(self,T,players,K,board:list,deck):
 
        for t in range(T):
            for p in range(len(players)):
                for k in range(K):
                    self.traversal([],p,players,board,t,10, 4,8,0,deck )
                # train model 
                self.value_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
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
        self.strat_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
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
            pred = self.strat_model.forward(cards,bets) # switch out when not exhuasted
            loss = self.strat_model.loss(pred,target_strategy,t_val)
            loss.backwards()
            optimizer.step()
        pass            

# g is actions i that round
    def traversal(self,h,p ,players,board,t,cur_bet, min_bet,max_bet,round,deck):
        if poker_game().is_terminal(round, len(players) ):
            return poker_game().util(h,p,players,board)
        # what does a chance node do in poker, it is adding a new card to the board
        elif poker_game().is_chance(players,round):
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
        
        elif poker_game().current_player(players).ID() == p:
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
                r.append( v[a] - v_o)
                pass

            labled_hole = self.process_card_labels(players[0].get_cards())
            tensor_hole = torch.tensor([labled_hole])
            labled_bets = self.history_to_bet(h)
            tensor_bets = torch.tensor([labled_bets])
            labled_board = self.process_card_labels(board)
            # should we include preflop            
            if len(labled_board) == 3:
                flop_cards = labled_board
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])
                self.m_v.append([cards_formatted,tensor_bets],t,torch.tensor([r]))
            elif len(labled_board) == 4:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn])
                self.m_v.append([cards_formatted,tensor_bets],t,torch.tensor([r]))
            elif  len(labled_board) == 5:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                river_card = labled_board[4]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                tensor_river = torch.tensor([river_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn,tensor_river])
                self.m_v.append([cards_formatted,tensor_bets],t,torch.tensor([r]))
            return v_o 
            #insert into m_V
        else:
            # Insert the infoset and its action probabilities (I, t, σt(I)) into the strategy memory MΠ
            # edit the regret_matching stuff so it uses the right cards

            o = None # add neural network
            labled_hole = self.process_card_labels(players[0].get_cards())
            tensor_hole = torch.tensor([labled_hole])
            labled_bets = self.history_to_bet(h)
            tensor_bets = torch.tensor([labled_bets])
            labled_board = self.process_card_labels(board)
            # should we include preflop
            if len(labled_board) == 3:
                flop_cards = labled_board
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])
                o = self.strat_model.forward(cards_formatted,tensor_bets)
                self.m_p.append([cards_formatted,tensor_bets],t,o)
            elif len(labled_board) == 4:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn])
                o = self.strat_model.forward(cards_formatted,tensor_bets)
                self.m_p.append([cards_formatted,tensor_bets],t,o)
            elif  len(labled_board) == 5:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                river_card = labled_board[4]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                tensor_river = torch.tensor([river_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn,tensor_river])
                o = self.strat_model.forward(cards_formatted,tensor_bets)
                self.m_p.append([cards_formatted,tensor_bets],t,o)
            A = self.get_actions(h)

            a = choices(A,o[0].tolist())
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
    def cards_to_num_dic_init(self,deck):
        counter = 0
        card_to_num_dic = {}
        for i in deck:
            card_to_num_dic[i] = counter
            counter +=1
        return card_to_num_dic

        
    def process_card_labels(self,cards):
        card_labels = []
        for i in cards:
            card_labels.append(self.card_to_label[i])
        return card_labels

    def history_to_bet(self, h):
        bets = []
        for i in h:
            if i == "bet":
                bets.append(1)
            else:
                bets.append(0)
        return self.bet_padding(bets)
    def bet_padding(self,bets:list):
        padding = [0 for i in range(BET_PADDING - len(bets))]
        return bets.extend(padding)
    
    

players = [Player(1, []),Player(2,[]), Player(3,[])]

print(poker_game().is_chance(players,0))
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