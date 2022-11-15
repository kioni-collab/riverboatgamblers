from Cards import Card, deck
from Players import player1, player2, player3

deck.shuffle()
print(deck)

while len(player1.hand) < 2:
    deck.deal(player1)
    deck.deal(player2)
    deck.deal(player3)

print(player1.hand)
print(player2.hand)
print(player3.hand)

print(deck)