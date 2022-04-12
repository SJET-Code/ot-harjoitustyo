import unittest
from blackjack import Deck, PlayingCard


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
    
    def test_created_deck_is_the_right_size(self):
        self.assertEqual(self.deck._size, 52)
    
    def test_function_get_card_decreases_deck_size(self):
        self.deck.get_card()
        self.assertEqual(self.deck._size, 51)

    def test_function_get_card_returns_PlayingCard_object(self):
        card=self.deck.get_card()
        self.assertTrue(type(card) is PlayingCard)
    
    def test_function_shuffle_resets_the_deck(self):
        self.deck.get_card()
        self.deck.get_card()
        self.deck.shuffle()
        self.assertEqual(self.deck._size, 52)