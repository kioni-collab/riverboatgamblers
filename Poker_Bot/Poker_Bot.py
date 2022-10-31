from parser import suite
import numpy as np
from random import randint
from enum import Enum
import itertools  
from itertools import permutations
from Card import card


NUM_ACTIONS = 4 # Raise,Call,Check,Fold - we change to be number of actions we have from unity 
NUM_CARDS = 52 # size of the deck
infoset_map = {}
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
            n = _N_ACTIONS
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

    


