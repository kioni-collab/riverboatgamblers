import random


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.showing = True

    def __repr__(self):
        value_name = {1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
                      10: 'Ten', 11: 'Jack', 12: 'Queen', 13: 'King'}
        if self.value in value_name:
            return value_name[self.value] + ' of ' + self.suit

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit


class StandardDeck(list):
    def __init__(self):
        for suit in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
            for value in range(1, 14):
                self.append(Card(value, suit))

    def shuffle(self):
        random.shuffle(self)
        print('Shuffling deck...')

    def deal(self, player):
        player.hand.append(self.pop(0))


deck = StandardDeck()

