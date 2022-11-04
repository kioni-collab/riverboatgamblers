from parser import suite
import numpy as np
from random import randint
from enum import Enum
import itertools  
from itertools import permutations
from Card import card


NUM_ACTIONS = 4 # Raise,Call,Check,Fold - we change to be number of actions we have from unity 
NUM_CARDS = 52 # size of the deck
infoset_map = {} # this is outside for continous training should also probabily pickle too
SUIT = ["H","S","D","C"]
RANK = ["A","1", "2","3","4","5","6","7","8","9","10","J","K","Q"]
DECK = set()


class game_node: 
    def _init_(self):
        self.infoset = None
        self.regretSum = np.zeros(NUM_ACTIONS)
        self.strategy = np.zeros(NUM_ACTIONS)
        self.strategySum = np.zeros(NUM_ACTIONS)
        self.reach_pr = 0
        self.reach_pr_sum = 0

    def next_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.strategy = self.calc_strategy()
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0
    
    def calc_strategy(self):
        strategy = self.make_positive(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy = strategy / total
        else:
            n = NUM_ACTIONS # change out later for paramter from unity 
            strategy = np.repeat(1/n, n)
        return strategy

    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        strategy = np.where(strategy < 0.001, 0, strategy)
        total = sum(strategy)
        strategy /= total
        return strategy
    def make_positive(self, x):
        return np.where(x > 0, x, 0)
    def __str__(self):
        strategies = ['{:03.2f}'.format(x) for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)

def cfr(history=[], cards = [[-1],[-1],[-1]], pr=[[1],[1],[1]] ,pr_c=1):
    # investigate pr_c more to see if it changes
    player_num = 1 # call to unity for which player
    info_set = get_info_set(cards[player_num], history)
    strategy = info_set.strategy
    info_set.reach_pr += pr[player_num]
    action_utils = np.zeros(NUM_ACTIONS) # change with actions given by unity
    actions_cur = ["fold","check","raise","call"] # will get from unity this is example
    for i, action in enumerate( actions_cur):
        next_history = history.append(action)
        pr_next  = list(pr)
        pr_next[player_num] = pr_next[player_num] * strategy[i] 
        action_utils[i] = -1 * cfr( next_history,cards,pr_next, pr_c)
    util = sum(action_utils * strategy)
    regrets = action_utils - util
    info_set.regret_sum += (np.prod(pr)/pr[player_num]) * pr_c * regrets
    return util
    
def get_info_set(cards,history):
    key = str(cards) + " " + str(history)
    info_set = None
    if key not in infoset_map:
      info_set = game_node(key)
      infoset_map[key] = info_set
      return info_set
    return infoset_map[key]

def __main__():
    # most of this will replaced with a call to unity 
    # to get what cards we have and other player
    unique_combin = [] 
    permut = permutations(SUIT,len(RANK))
    for comb in permut:
        zipped = zip(comb,RANK)
        [unique_combin.append(i) for i in zipped]

    for i in unique_combin:
        DECK.add(card(i))
    cards_1 = [DECK.pop() for i in range(2)]
    cards_2 = [DECK.pop() for i in range(2)]

    


