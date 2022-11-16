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
player3 = Player('Kioni')
players = [player1, player2, player3]


def assign_player_roles(players_not_out):
    index = 0
    dealer = players_not_out[index]
    dealer.roles_list.append('dealer')
    index += 1
    index %= len(players_not_out)
    small_blind = players_not_out[index]
    small_blind.roles_list.append('small blind')
    index += 1
    index %= len(players_not_out)
    big_blind = players_not_out[index]
    big_blind.roles_list.append('big blind')
    index += 1
    index %= len(players_not_out)
    first_to_act = players_not_out[index]
    first_to_act.roles_list.append('first to act')
    players_not_out.append(players_not_out.pop(0))


assign_player_roles(players)