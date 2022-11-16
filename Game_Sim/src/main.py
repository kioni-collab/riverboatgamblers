from Cards import Card, deck
from Players import Player, player1, player2, player3

players = [player1, player2, player3]
deck.shuffle()

while len(player1.hand) < 2:
    deck.deal(player1)
    deck.deal(player2)
    deck.deal(player3)

print('\n')
print(player1.name, player1.hand)
print(player2.name, player2.hand)
print(player3.name, player3.hand)
print('\n')

#print the roles of each player
for player in players:
    print(player.name, player.roles_list)

# pre flop over when everyone has folded or put the same amount of chips in the pot


class Game(object):
    def __init__(self):
       self.cards_on_table = []
       self.pot = 0
       self.blind_amounts = [10, 20]
       self.game_over = False
       self.pot = 0

    def start_game(self):
        print('\n')
        print('Welcome to Texas Holdem!')
        print('The game is starting...')
        print('\n')