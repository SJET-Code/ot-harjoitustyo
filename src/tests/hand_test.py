import unittest
from blackjack.player import Player
from blackjack.playing_card import PlayingCard
from blackjack.hand import Hand

class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand(10, Player())

    def test_creating_a_hand_takes_bet_amount_from_player_credits(self):
        self.assertEqual(self.hand._player.credits(), 90)
    
    def test_add_card_does_ace_change_when_hand_value_is_over_21(self):
        self.hand.starting_deal(PlayingCard(11,'SA'),PlayingCard(11,'CA'))
        self.hand.add_card(PlayingCard(11,'HA'))
        self.assertEqual(self.hand.value(),13)
    
    def test_starting_deal_turns_can_split_true_when_same_card_value(self):
        self.hand.starting_deal(PlayingCard(10,'SK'),PlayingCard(10,'SQ'))
        self.assertTrue(self.hand.can_split())
    
    def test_split_decreases_hands_cards(self):
        self.hand.starting_deal(PlayingCard(10,'SK'),PlayingCard(10,'SQ'))
        self.hand.split()
        self.assertEqual(len(self.hand.cards()), 1)