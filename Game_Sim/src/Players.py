class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.hand = [] # list of cards the player has
        self.score = []
        self.chips = 0
        self.stake = 0
        self.stake_gap = 0 # this is the amount the player has to pay to stay in the round
        self.fold = False
        self.ready = False
        self.all_in = False
        self.roles_list = []
        self.win = False


player1 = Player('Logan')
player2 = Player('Natalie')
player3 = Player('Killer AI')