import numpy as np
from random import randint

NUM_ACTIONS = 4 # Raise,Call,Check,Fold - may be problematic since not all 4 are avaivle always
NUM_CARDS = 52 # size of the deck
infoset_map = {}
class game_node: 
    def _init_(self):
        self.infoset = None
        
