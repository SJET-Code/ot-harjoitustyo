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

    def test_double_down_returns_false_when_player_doesnt_have_enough_credits(self):
        self.hand = Hand(60, Player())
        self.assertFalse(self.hand.double_down())

    def test_stay_is_true_after_add_card_and_double_down(self):
        self.hand.starting_deal(PlayingCard(5, 'S5'), PlayingCard(5, 'C5'))
        self.hand.double_down()
        self.hand.add_card(PlayingCard(11, 'SA'))
        self.assertTrue(self.hand.stay())

    def test_payout_pays_player_correctly_on_point_win(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(10, 'CK'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(7, 'S7')], 17)
        self.assertEqual(self.hand._player.credits(), 110)

    def test_payout_pays_player_correctly_on_dealer_bust_out(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(10, 'CK'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(5, 'S5'), PlayingCard(10, 'HJ')], 25)
        self.assertEqual(self.hand._player.credits(), 110)

    def test_payout_pays_player_correctly_on_blackjack_win(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(11, 'CA'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(5, 'S5'), PlayingCard(10, 'HJ')], 25)
        self.assertEqual(self.hand._player.credits(), 115)

    def test_payout_pays_player_correctly_on_blackjack_draw(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(11, 'CA'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(11, 'HA')], 21)
        self.assertEqual(self.hand._player.credits(), 100)

    def test_win_function_returns_false_when_hand_hasnt_been_resolved(self):
        self.assertFalse(self.hand.win())

    def test_win_function_returns_true_when_hand_has_been_resolved(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(11, 'CA'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(5, 'S5'), PlayingCard(6, 'H6')], 21)
        self.assertTrue(self.hand.win())

    def test_win_message_function_returns_empty_string_when_hand_hasnt_resolved(self):
        self.assertEqual(self.hand.win_message(), '')

    def test_win_message_function_returns_string_when_hand_has_resolved(self):
        self.hand.starting_deal(PlayingCard(10, 'SJ'), PlayingCard(11, 'CA'))
        self.hand.stand()
        self.hand.payout([PlayingCard(10, 'HQ'), PlayingCard(5, 'S5'), PlayingCard(6, 'H6')], 21)
        self.assertIsInstance(self.hand.win_message(), str)
