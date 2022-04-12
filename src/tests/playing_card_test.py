import unittest
from blackjack import PlayingCard


class TestPlayingCard(unittest.TestCase):
    def setUp(self):
        self.card = PlayingCard(11, 'SA')

    def test_cards_value_is_correct(self):
        self.assertEqual(self.card.value(), 11)

    def test_cards_crest_is_correct(self):
        self.assertEqual(self.card.crest(), 'SA')

    def test_ace_change_works_correctly(self):
        self.card.ace_change()
        self.assertEqual(self.card.value(), 1)
