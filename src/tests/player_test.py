import unittest
from blackjack.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_starting_credits_are_correct(self):
        self.assertEqual(self.player.credits(), 100)

    def test_betting_takes_out_the_right_amount_of_credits(self):
        self.player.bet(45)
        self.assertEqual(self.player.credits(), 55)

    def test_cant_bet_more_credits_than_you_have(self):
        self.player.bet(1000)
        self.assertEqual(self.player.credits(), 100)

    def test_return_false_when_bet_is_not_possible(self):
        self.assertFalse(self.player.bet(1000))

    def test_payout_increases_credits_correctly(self):
        self.player.payout(100)
        self.assertEqual(self.player.credits(), 200)

    def test_reset_sets_credits_back_to_default_amount(self):
        self.player.payout(10000)
        self.player.bet(300)
        self.player.reset()
        self.assertEqual(self.player.credits(), 100)
