import unittest
from blackjack.round import Round
from blackjack.player import Player
from blackjack.deck import Deck
from blackjack.playing_card import PlayingCard
from blackjack.hand import Hand


class TestRound(unittest.TestCase):
    def setUp(self):
        self.round = Round(Player(),Deck())
    
    def test_function_add_player_hand_increases_player_hands_lenght(self):
        self.round.add_player_hand(10)
        self.assertEqual(len(self.round._player_hands), 1)
    
    def test_funtion_new_round_deal_gives_player_hands_2_cards(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertEqual(len(self.round._player_hands[0].cards()), 2)

    def test_funtion_new_round_deal_gives_a_card_to_dealer(self):
        self.round.new_round_deal()
        self.assertEqual(len(self.round._dealer_hand), 1)
    
    def test_funtion_new_round_assigns_dealer_card(self):
        self.round.new_round_deal()
        self.assertIsNotNone(self.round._dealer_card)
    
    def test_funtion_hit_increases_player_hand_size(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.hit()
        self.assertEqual(len(self.round._player_hands[0].cards()),3)
    
    def test_function_hit_return_true_when_no_player_hands(self):
        self.assertTrue(self.round.hit())

    def test_function_hit_return_false_when_active_hands_left(self):
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertFalse(self.round.hit())

    def test_function_hit_return_true_when_no_active_hands_left(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        while not self.round._player_hands[0].bust():
            self.round.hit()
        self.assertTrue(self.round.hit())

    def test_function_check_split_return_False_when_over_4_hands(self):
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.assertFalse(self.round.check_split())

    def test_function_check_split_return_true_when_can_split_hand(self):
        self.round.add_player_hand(10)
        self.round._player_hands[0].starting_deal(PlayingCard(10,'SK'),PlayingCard(10,'SJ'))
        self.assertTrue(self.round.check_split())

    def test_function_check_split_return_false_when_cant_split_hand(self):
        self.round.add_player_hand(10)
        self.round._player_hands[0].starting_deal(PlayingCard(11,'SA'),PlayingCard(10,'SJ'))
        self.assertFalse(self.round.check_split())

    def test_function_check_split_return_false_when_no_active_hand(self):
        self.assertFalse(self.round.check_split())

    def test_function_split_adds_new_hand(self):
        self.round.add_player_hand(10)
        self.round._player_hands[0].starting_deal(PlayingCard(10,'SK'),PlayingCard(10,'SJ'))
        self.round.split()
        self.assertEqual(len(self.round._player_hands), 2)

    def test_function_stay_returns_true_when_no_more_active_hands(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertTrue(self.round.stay())

    def test_function_stay_returns_true_when_no_hands(self):
        self.assertTrue(self.round.stay())

    def test_function_stay_returns_flase_when_more_active_hands(self):
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertFalse(self.round.stay())

    def test_function_split_doesnt_add_new_hand_when_no_active_hand(self):
        self.round.split()
        self.assertEqual(len(self.round._player_hands), 0)

    def test_function_reset_resets_player_hands_and_dealer_hand_and_value(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.dealer_deal()
        self.round.reset()
        self.assertEqual((self.round._player_hands,self.round._dealer_hand,self.round._dealer_hand_value, self.round._dealer_card),([], [], 0, None))

    def test_function_player_hands_returns_list(self):
        test=self.round.player_hands()
        self.assertTrue(type(test)==list)

    def test_function_dealer_hand_returns_tuple(self):
        test=self.round.dealer_hand()
        self.assertTrue(type(test)==tuple)

    def test_function_dealer_hand_returns_tuple_with_list_of_cards(self):
        test=self.round.dealer_hand()[0]
        self.assertIs(test,self.round._dealer_hand)

    def test_function_dealer_hand_returns_tuple_with_int_of_dealer_hand_value(self):
        test=self.round.dealer_hand()[1]
        self.assertIs(test,self.round._dealer_hand_value)

    def test_function_check_for_aces_does_ace_change_correctly_for_dealer(self):
        self.round._dealer_hand.append(PlayingCard(11,'SA'))
        self.round._dealer_hand_value+=11
        self.round._check_for_aces()
        self.assertEqual(1,self.round._dealer_hand_value)
    
    def test_function_dealer_deal_checks_for_aces_when_dealer_hand_value_is_over_21(self):
        self.round._dealer_card = PlayingCard(11,'SA')
        self.round._dealer_hand.append(PlayingCard(11,'SA'))
        self.round._dealer_hand_value+=11
        test = self.round._dealer_hand_value+11
        self.round.dealer_deal()
        self.assertEqual(test-10, self.round._dealer_hand_value)

    def test_function_dealer_deal_returns_false_when_dealer_hand_value_under_17(self):
        self.round._dealer_card = PlayingCard(2,'S2')
        self.round._dealer_hand.append(PlayingCard(2,'C2'))
        self.round._dealer_hand_value+=2
        self.assertFalse(self.round.dealer_deal())

    def test_function_check_bust_true_when_no_hands(self):
        self.assertTrue(self.round.check_bust())

    def test_function_check_bust_returns_false_when_active_hands_that_have_not_busted(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertFalse(self.round.check_bust())

    def test_function_check_bust_returns_true_when_all_hands_busted(self):
        self.round.add_player_hand(10)
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        while not self.round._player_hands[1].bust():
            self.round.hit()
        self.assertTrue(self.round.check_bust())
    
    def test_function_check_surrender_returns_true_when_can_surrender(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertTrue(self.round.check_surrender())

    def test_function_check_surrender_returns_false_when_cant_surrender(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.hit()
        self.assertFalse(self.round.check_surrender())

    def test_function_check_surrender_returns_false_when_no_hands(self):
        self.assertFalse(self.round.check_surrender())
    
    def test_function_surrender_hand_surrenders_hand(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.surrender_hand()
        self.assertTrue(self.round._player_hands[0].surrender())

    def test_function_check_double_down_returns_true_when_can_double_down(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.assertTrue(self.round.check_double_down())

    def test_function_check_double_down_returns_false_when_cant_double_down(self):
        self.round.add_player_hand(60)
        self.round.new_round_deal()
        self.assertFalse(self.round.check_double_down())

    def test_function_check_double_down_returns_false_when_no_hand(self):
        self.assertFalse(self.round.check_double_down())

    def test_function_double_down_works_when_can_double_down(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.double_down()
        self.assertEqual(self.round._player_hands[0].bet(),20)

    def test_function_double_down_doesnt_works_when_cant_double_down(self):
        self.round.add_player_hand(10)
        self.round.new_round_deal()
        self.round.stay()
        self.round.double_down()
        self.assertEqual(self.round._player_hands[0].bet(),10)
    
    def test_function_player_returns_player_object(self):
        self.assertTrue(type(self.round.player()) == Player)