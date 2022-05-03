import unittest
from blackjack.deck import Deck
from blackjack.playing_card import PlayingCard

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
    
    def test_function_get_card_shuffles_the_deck_when_less_than_13_cards(self):
        for i in range(41):
            self.deck.get_card()
        self.assertEqual(self.deck._size, 51)