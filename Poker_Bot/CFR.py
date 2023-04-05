from Model import DeepCFRModel 
import numpy as np 
from random import choices
import random
from torch import optim
from player import Player
import torch
from pokergame import poker_game
from pokerface import *
import copy 

BET_PADDING = 1000
CARD_TYPES = 2
NACTIONS = 3
class CFR():
    def __init__(self,player_num):
        self.m_v = [[] for p in range(player_num)]
        self.m_pi = []
        self.value_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
        self.strat_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
        self.card_to_label = self.cards_to_num_dic_init(StandardDeck())


    # TODO 
    # figure out how to split infoset to be cards in hand, cards on board and betting postions
    # may need to change how we pass network parametrs through traversal
    # may need infoset map as well
    # find out if models are already initialized to return 0 
    def deepcfr(self,T,player_num,K):
 
        for t in range(1,T+1):
            deck = StandardDeck()
            players = [Player(i,deck.draw(2)) for i in range(player_num)]
            board = []
            print(players)
            for p in range(len(players)):
                for k in range(K):
                    print(p,k)
                    self.traversal([],p,players,board,t,10, 4,8,1,copy.deepcopy(deck),0,players)
                # train model 
                self.value_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
                optimizer = optim.Adam(self.value_model.parameters())
                cards = [i[0][0] for i in self.m_v[p]]
                bets = [i[0][1] for i in self.m_v[p]]
                target_regret = [i[2] for i in self.m_v[p]]
                t_val = [i[1] for i in self.m_v[p]]
                # print(p)
                # print(self.m_v[p])
                # card_format = cards[0]
                # for c in cards[2:]:
                #     card_format = torch.cat((card_format,c),0)
                # print(card_format)
                for e in range(100):
                    all_diff_tensor = torch.empty((0,3), dtype=torch.float32)
                    for c,b,tr,tv in zip(cards,bets, target_regret,t_val):
                        optimizer.zero_grad()
                        pred = self.value_model(c,b) # switch out when not exhuasted
                        all_diff_tensor = torch.cat((all_diff_tensor, pred-tr ), 0) 
                        loss = self.strat_model.loss(pred,tr,tv)
                        loss.backward(retain_graph=True)
                        optimizer.step()
                    print("player:", p, "Poker_regret_Model","Epoch", e, "RSME",torch.sqrt(torch.mean(torch.sum(torch.square(all_diff_tensor),1))).item())
                    torch.save(self.value_model.state_dict(), "Poker_regret_Model")
        self.strat_model = DeepCFRModel(CARD_TYPES,BET_PADDING,NACTIONS)
        optimizer = optim.Adam(self.strat_model.parameters())
        cards = [i[0][0] for i in self.m_pi]
        bets = [i[0][1] for i in self.m_pi]
        target_strategy = [i[2] for i in self.m_pi]
        t_val = [i[1] for i in self.m_pi]
       # print(cards)
        # card_format = cards[0]
        # for c in cards:
        #     print("gg")
        #     print(card_format)
        #     print(c)
        #     card_format = torch.cat((card_format,c),0)
        # print(card_format)
        for e in range(100):
            all_diff_tensor = torch.empty((0,3), dtype=torch.float32)
            for c,b,ts,tv in zip(cards,bets, target_strategy,t_val):
                optimizer.zero_grad()
                pred = self.strat_model.forward(c,b) # switch out when not exhuasted
                all_diff_tensor = torch.cat((all_diff_tensor, pred-ts ), 0) 
                loss = self.strat_model.loss(pred,ts,tv)
                loss.backward(retain_graph=True)
                optimizer.step() 
            print("Poker_strategy_Model","Epoch", e, "RSME",torch.sqrt(torch.mean(torch.sum(torch.square(all_diff_tensor),1))).item())
            torch.save(self.strat_model.state_dict(), "Poker_strategy_Model")
        pass            

# g is actions i that round
    def traversal(self,h,p ,players,board,t,cur_bet, min_bet,max_bet,round,deck,depth, all_players):
        if depth >= 40:
            print("Depth kill")
            return 0
        if poker_game().is_terminal(round, len(players), board ):
          
            return poker_game().util(h,p,players,board,all_players)
        # what does a chance node do in poker, it is adding a new card to the board
        elif poker_game().is_chance(players):
            # get number of cards left in deck
            # pick one randomly
            # add to board and history
            # done
            
            if round == 1:
                board = deck.draw(3)
            else:
                board.append(deck.draw(1)[0])
            h.append("board_card")
            #reset all player actions to none
            new_players = list(players)
            for pl in new_players:
                pl.set_last_action(None) 

            round += 1
            depth += 1
            return self.traversal(h,p ,new_players,board,t,cur_bet, min_bet,max_bet,round,copy.deepcopy(deck), depth, all_players) 
        
        elif poker_game().current_player(players).ID() == p:
            # make a regret matching function
            r_net = None # add neural network
            labled_hole = self.process_card_labels(players[0].get_cards())
            tensor_hole = torch.tensor([labled_hole])

            labled_bets = self.history_to_bet(h)
            tensor_bets = torch.tensor([labled_bets])
            
            labled_board = self.process_card_labels(board)
            # should we include preflop
            if len(labled_board) == 0:
                flop_cards = [-1,-1,-1]
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])

                r_net = self.value_model.forward(cards_formatted,tensor_bets)
               


            elif len(labled_board) == 3:
                flop_cards = labled_board
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])
                r_net = self.value_model.forward(cards_formatted,tensor_bets)
            elif len(labled_board) == 4:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn])
                r_net = self.value_model.forward(cards_formatted,tensor_bets)
            elif  len(labled_board) == 5:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                river_card = labled_board[4]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                tensor_river = torch.tensor([river_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn,tensor_river])
                r_net = self.strat_model.forward(cards_formatted,tensor_bets)
            
            o = {}

            v = {}
            v_o = 0
            r = []
            actions = poker_game().get_actions(players,round)
            o_net = self.regret_matching(r_net,actions)
            print(o_net)
            print(actions)
            for i in range(len(actions)):
                o[actions[i]] = o_net[0].tolist()[i]
            
            for a in actions:
                h_new = list(h)
                h_new.append(a)
                new_players = list(players)
                new_players[0].set_last_action(a)
                new_all_players = list(all_players)
                if a == "bet":
                    if round < 3:
                        cur_bet += min_bet
                    else:
                        cur_bet += max_bet
                    new_players[0].set_bet_amt(cur_bet)
                    new_all_players[self.get_player_idx(new_players[0].ID(),new_all_players)].set_bet_amt(cur_bet) 
                elif a == "call":
                    new_players[0].set_bet_amt(cur_bet)
                    new_all_players[self.get_player_idx(new_players[0].ID(),new_all_players)].set_bet_amt(cur_bet) 
                
                if a == "fold":
                    
                    new_players = new_players[1:]
                else:
                    last_player = new_players[0]
                    new_players = new_players[1:]
                    new_players.append(last_player)
                
                depth += 1
                v[a] = self.traversal(h_new,p,new_players,board,t,cur_bet, min_bet, max_bet, round,copy.deepcopy(deck),depth,new_all_players)
                
                v_o += o[a] * v[a]
            for a in actions:
                #work out what data type r(I,a) should be
                r.append( v[a] - v_o)
                pass

            labled_hole = self.process_card_labels(players[0].get_cards())
            tensor_hole = torch.tensor([labled_hole])
            labled_bets = self.history_to_bet(h)
            tensor_bets = torch.tensor([labled_bets])
            labled_board = self.process_card_labels(board)
            # should we include preflop   
            if len(labled_board) == 0:
                flop_cards = [-1,-1,-1]
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])

                o = self.strat_model.forward(cards_formatted,tensor_bets)
                self.m_v[p].append([[cards_formatted,tensor_bets],t,o])         
            if len(labled_board) == 3:
                flop_cards = labled_board
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])
                self.m_v[p].append([[cards_formatted,tensor_bets],t,torch.tensor([r])])
            elif len(labled_board) == 4:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn])
                self.m_v[p].append([[cards_formatted,tensor_bets],t,torch.tensor([r])])
            elif  len(labled_board) == 5:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                river_card = labled_board[4]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                tensor_river = torch.tensor([river_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn,tensor_river])
                self.m_v[p].append([[cards_formatted,tensor_bets],t,torch.tensor([r])])
            return v_o 
            #insert into m_V
        else:
            # Insert the infoset and its action probabilities (I, t, σt(I)) into the strategy memory MΠ
            # edit the regret_matching stuff so it uses the right cards

            r_net = None # add neural network
            labled_hole = self.process_card_labels(players[0].get_cards())
            tensor_hole = torch.tensor([labled_hole])

            labled_bets = self.history_to_bet(h)
            tensor_bets = torch.tensor([labled_bets])
            
            labled_board = self.process_card_labels(board)
            # should we include preflop
            A = poker_game().get_actions(players,round)
            
            if len(labled_board) == 0:
                flop_cards = [-1,-1,-1]
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])

                r_net = self.strat_model.forward(cards_formatted,tensor_bets)
                o = self.regret_matching(r_net,A)
                self.m_pi.append([[cards_formatted,tensor_bets],t,o])


            elif len(labled_board) == 3:
                flop_cards = labled_board
                tensor_flop = torch.tensor([flop_cards])
                cards_formatted = (tensor_hole,tensor_flop,[])
                r_net = self.strat_model.forward(cards_formatted,tensor_bets)
                o = self.regret_matching(r_net,A)
                self.m_pi.append([[cards_formatted,tensor_bets],t,o])
            elif len(labled_board) == 4:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn])
                r_net = self.strat_model.forward(cards_formatted,tensor_bets)
                o = self.regret_matching(r_net,A)
                self.m_pi.append([[cards_formatted,tensor_bets],t,o])
            elif  len(labled_board) == 5:
                flop_cards = labled_board[:3]
                turn_card = labled_board[3]
                river_card = labled_board[4]
                tensor_flop = torch.tensor([flop_cards])
                tensor_turn = torch.tensor([turn_card])
                tensor_river = torch.tensor([river_card])
                cards_formatted = (tensor_hole,tensor_flop,[tensor_turn,tensor_river])
                r_net = self.strat_model.forward(cards_formatted,tensor_bets)
                o = self.regret_matching(r_net,A)
                self.m_pi.append([[cards_formatted,tensor_bets],t,o])
            
            print(o)
            a = choices(A,o[0].tolist())[0]
            
            h_new = list(h)
            h_new.append(a)
            new_players = list(players)
            new_players[0].set_last_action(a)
            new_all_players = list(all_players)
            if a == "bet":
                if round < 3:
                    cur_bet += min_bet
                else:
                    cur_bet += max_bet
                new_players[0].set_bet_amt(cur_bet)
                new_all_players[self.get_player_idx(new_players[0].ID(),new_all_players)].set_bet_amt(cur_bet) 
            elif a == "call":
                new_players[0].set_bet_amt(cur_bet)
                new_all_players[self.get_player_idx(new_players[0].ID(),new_all_players)].set_bet_amt(cur_bet) 
            if a == "fold":
                
                new_players = new_players[1:]
            else:
                last_player = new_players[0]
                new_players = new_players[1:]
                new_players.append(last_player)
            
            depth += 1
            return self.traversal(h_new,p,new_players,board,t,cur_bet, min_bet,max_bet,round,copy.deepcopy(deck), depth, new_all_players)

            pass
    def get_player_idx(self,p, players):
        index  = -1
        for i in range(len(players)):
            if players[i].ID() == p:
                index = i
        return index
    
    def regret_matching(self, reg, actions):
        print(reg)
        reg[reg<0] = 0
        print(reg)
        if torch.sum(reg) > 0:

            return torch.div(reg,torch.sum(reg))
        else:
            act = [1/len(actions) for i in range(len(actions))]
            print("non neg ",torch.tensor([act]) )
            return torch.tensor([act])

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
        bets.extend(padding)
        return bets
    
    

players = [Player(1, []),Player(2,[]), Player(3,[])]

print(poker_game().is_chance(players))
hole = [[1,2]]
print(torch.tensor(hole).shape)
board = [[3, 4,5,6]]
turn = [[7]]
cards = ( torch.tensor(hole),torch.tensor(board), [torch.tensor(turn)])
#mase sure there is enough buffering/padding for bets 
bets = [[0,-1,0,-1,-1, 0, 0,0,0,0]]
print(DeepCFRModel(2,10,4).forward(cards,torch.tensor(bets) ))

# bets1 = [[0,-1,0,-1,-1]]
# print(DeepCFRModel(2,5,4).forward(cards,torch.tensor(bets1) ))

# print(DeepCFRModel(2,10,4).loss(DeepCFRModel(2,10,4).forward(cards,torch.tensor(bets) ),DeepCFRModel(2,5,4).forward(cards,torch.tensor(bets1) ),2).backward)
# optimizer = optim.Adam(DeepCFRModel(2,10,4).parameters())

# optimizer.zero_grad()
# DeepCFRModel(2,10,4).loss(DeepCFRModel(2,10,4).forward(cards,torch.tensor(bets) ),DeepCFRModel(2,5,4).forward(cards,torch.tensor(bets1) ),2).backward

# optimizer.step()

CFR(3).deepcfr(20,3,12)