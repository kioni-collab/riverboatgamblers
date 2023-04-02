from player import Player
from pokergame import poker_game
from pokerface import *

def test_round_not_over_two_player_start():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_1.set_bet_amt(0)
    player_1.set_last_action(None)
    player_2.set_bet_amt(0)
    player_2.set_last_action(None)
    assert poker_game().is_chance([player_1,player_2]) == False

def test_round_not_over_three_player_start():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(0)
    player_1.set_last_action(None)
    player_2.set_bet_amt(0)
    player_2.set_last_action(None)
    player_3.set_bet_amt(0)
    player_3.set_last_action(None)
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_diff_bets():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(2)
    player_1.set_last_action(None)
    player_2.set_bet_amt(4)
    player_2.set_last_action(None)
    player_3.set_bet_amt(4)
    player_3.set_last_action("call")
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_same_bets():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(4)
    player_1.set_last_action(None)
    player_2.set_bet_amt(4)
    player_2.set_last_action(None)
    player_3.set_bet_amt(4)
    player_3.set_last_action("call")
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_3():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(2)
    player_1.set_last_action("call")
    player_2.set_bet_amt(4)
    player_2.set_last_action(None)
    player_3.set_bet_amt(8)
    player_3.set_last_action("bet")
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_4():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(8)
    player_1.set_last_action("call")
    player_2.set_bet_amt(4)
    player_2.set_last_action("fold")
    player_3.set_bet_amt(8)
    player_3.set_last_action("bet")
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_5():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(8)
    player_1.set_last_action("check")
    player_2.set_bet_amt(8)
    player_2.set_last_action(None)
    player_3.set_bet_amt(8)
    player_3.set_last_action(None)
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_6():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("call")
    player_3.set_bet_amt(8)
    player_3.set_last_action(None)
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_not_over_three_player_7():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("call")
    player_3.set_bet_amt(16)
    player_3.set_last_action("bet")
    assert poker_game().is_chance([player_1,player_2,player_3]) == False

def test_round_over_three_player_1():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(8)
    player_1.set_last_action("call")
    player_2.set_bet_amt(4)
    player_2.set_last_action("fold")
    player_3.set_bet_amt(8)
    player_3.set_last_action("bet")
    # by the time this function is called players who folded 
    #already removed from player list 
    assert poker_game().is_chance([player_1,player_3]) == True

def test_round_over_three_player_2():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(8)
    player_1.set_last_action("call")
    player_2.set_bet_amt(8)
    player_2.set_last_action("call")
    player_3.set_bet_amt(8)
    player_3.set_last_action("bet")
    assert poker_game().is_chance([player_1, player_2,player_3]) == True

def test_round_over_three_player_3():
    player_1 = Player(1,[])
    player_2 = Player(2,[])
    player_3 = Player(3,[])
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("call")
    player_3.set_bet_amt(12)
    player_3.set_last_action("call")
    assert poker_game().is_chance([player_1, player_2,player_3]) == True

def test_util_loose():
    deck = StandardDeck()
    board = deck.draw(parse_cards('Jc3d5c4hJh'))
    player_1 = Player(1,deck.draw(parse_cards('2dAc')))
    player_2 = Player(2,deck.draw(parse_cards('5h7s')))
    player_3 = Player(3,deck.draw(parse_cards('7h6h')))
    print("this good")
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("call")
    player_3.set_bet_amt(12)
    player_3.set_last_action("call")
    assert poker_game().util([], 1,[player_1,player_2,player_3],board, [player_1,player_2,player_3]) == -12

def test_util_win():
    deck = StandardDeck()
    board = deck.draw(parse_cards('Jc3d5c4hJh'))
    player_1 = Player(1,deck.draw(parse_cards('2dAc')))
    player_2 = Player(2,deck.draw(parse_cards('5h7s')))
    player_3 = Player(3,deck.draw(parse_cards('7h6h')))
    print("this good")
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("call")
    player_3.set_bet_amt(12)
    player_3.set_last_action("call")
    assert poker_game().util([], 3,[player_1,player_2,player_3],board,[player_1,player_2,player_3]) == 24

def test_util_fold_lose():
    deck = StandardDeck()
    board = deck.draw(parse_cards('Jc3d5c4hJh'))
    player_1 = Player(1,deck.draw(parse_cards('2dAc')))
    player_2 = Player(2,deck.draw(parse_cards('5h7s')))
    player_3 = Player(3,deck.draw(parse_cards('7h6h')))
    print("this good")
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("fold")
    player_3.set_bet_amt(12)
    player_3.set_last_action("fold")
    assert poker_game().util([], 3,[player_1],board,[player_1,player_2,player_3]) == -12

def test_util_fold_win():
    deck = StandardDeck()
    board = deck.draw(parse_cards('Jc3d5c4hJh'))
    player_1 = Player(1,deck.draw(parse_cards('2dAc')))
    player_2 = Player(2,deck.draw(parse_cards('5h7s')))
    player_3 = Player(3,deck.draw(parse_cards('7h6h')))
    print("this good")
    player_1.set_bet_amt(12)
    player_1.set_last_action("bet")
    player_2.set_bet_amt(12)
    player_2.set_last_action("fold")
    player_3.set_bet_amt(12)
    player_3.set_last_action("fold")
    assert poker_game().util([], 1,[player_1],board,[player_1,player_2,player_3]) == 24