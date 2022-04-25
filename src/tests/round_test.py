import unittest
from blackjack import Round, Player,Deck,PlayingCard


class TestRound(unittest.TestCase):
    def setUp(self):
        self.round = Round(Player(),Deck())
    
    def test_function_new_round_assigns_bet_correctly(self):
        self.round.new_round(25)
        self.assertEqual(self.round._bet,25)
    
    def test_funtion_new_round_deals_two_cards_to_player(self):
        self.round.new_round(25)
        self.assertEqual(len(self.round._player_hand), 2)

    def test_funtion_new_round_deals_a_card_to_dealer(self):
        self.round.new_round(25)
        self.assertEqual(len(self.round._dealer_hand), 1)
    
    def test_funtion_new_round_assigns_dealer_card_value(self):
        self.round.new_round(25)
        self.assertIsNotNone(self.round._dealer_card)
    
    def test_funtion_hit_increases_player_hand_size(self):
        self.round.new_round(25)
        self.round.hit()
        self.assertEqual(len(self.round._player_hand),3)
    
    def test_function_stay_increases_dealer_hand_size(self):
        self.round.new_round(25)
        self.round.stay()
        self.assertEqual(len(self.round._dealer_hand),2)

    def test_function_dealer_deal_increases_dealer_hand_size_if_dealer_hand_value_is_less_than_17(self):
        self.round.new_round(25)
        self.round.stay()
        exeption=self.round._dealer_hand_value>=17
        self.round.dealer_deal()
        self.assertTrue(len(self.round._dealer_hand)==3 or exeption)

    def test_function_dealer_deal_returns_correct_number_based_on_dealer_hand_value(self):
        self.round.new_round(25)
        self.round.stay()
        answer=self.round.dealer_deal()
        self.assertTrue(self.round._dealer_hand_value<17 and answer==2 or 16<self.round._dealer_hand_value<=21 and (answer==1 or answer==0) or 
        self.round._dealer_hand_value>21 and answer==1)

    def test_function_count_payout_pays_correct_amount_when_player_doesnt_have_blackjack(self):
        self.round.new_round(25)
        for card in self.round._player_hand:
            if card.value()==11:
                card.ace_change()
        self.round.count_payout()
        self.assertEqual(self.round._player.credits(),125)

    def test_function_count_payout_pays_correct_amount_when_player_has_blackjack(self):
        self.round.new_round(25)
        self.round._player_hand_value=21
        self.round.count_payout()
        self.assertEqual(self.round._player.credits(),137)
    
    def test_function_reset_resets_player_and_dealer_hand_and_values(self):
        self.round.new_round(25)
        self.round.stay()
        self.round.reset()
        self.assertEqual((self.round._player_hand,self.round._player_hand_value,self.round._dealer_hand,self.round._dealer_hand_value),([],0,[],0))

    def test_function_player_hand_returns_tuple(self):
        self.round.new_round(25)
        test=self.round.player_hand()
        self.assertTrue(type(test)==tuple)

    def test_function_player_hand_returns_tuple_with_list_of_cards(self):
        self.round.new_round(25)
        test=self.round.player_hand()[0]
        self.assertIs(test,self.round._player_hand)

    def test_function_player_hand_returns_tuple_with_int_of_player_hand_value(self):
        self.round.new_round(25)
        test=self.round.player_hand()[1]
        self.assertIs(test,self.round._player_hand_value)

    def test_function_dealer_hand_returns_tuple(self):
        self.round.new_round(25)
        test=self.round.dealer_hand()
        self.assertTrue(type(test)==tuple)

    def test_function_dealer_hand_returns_tuple_with_list_of_cards(self):
        self.round.new_round(25)
        test=self.round.dealer_hand()[0]
        self.assertIs(test,self.round._dealer_hand)

    def test_function_dealer_hand_returns_tuple_with_int_of_dealer_hand_value(self):
        self.round.new_round(25)
        test=self.round.dealer_hand()[1]
        self.assertIs(test,self.round._dealer_hand_value)
    
    def test_function_check_for_aces_does_ace_change_correctly_for_player(self):
        self.round.new_round(25)
        self.round._player_hand.append(PlayingCard(11,'SA'))
        self.round._player_hand_value+=11
        test=self.round._player_hand_value
        self.round.check_for_aces(1)
        self.assertEqual(test-10,self.round._player_hand_value)

    def test_function_check_for_aces_does_ace_change_correctly_for_dealer(self):
        self.round.new_round(25)
        self.round._dealer_hand.append(PlayingCard(11,'SA'))
        self.round._dealer_hand_value+=11
        test=self.round._dealer_hand_value
        self.round.check_for_aces(0)
        self.assertEqual(test-10,self.round._dealer_hand_value)
    
    def test_function_hit_checks_for_aces_when_player_hand_value_is_over_21(self):
        self.round.new_round(25)
        self.round._player_hand.append(PlayingCard(11,'SA'))
        self.round._player_hand_value+=11
        while self.round._player_hand_value<=21:
            self.round._player_hand.append(PlayingCard(11,'SA'))
            self.round._player_hand_value+=11
        test = self.round._player_hand_value
        self.round.hit()
        test += self.round._player_hand[-1].value()
        self.assertEqual(test-10, self.round._player_hand_value)

    def test_function_stay_checks_for_aces_when_dealer_hand_value_is_over_21(self):
        self.round.new_round(25)
        self.round._dealer_card = PlayingCard(11,'SA')
        while self.round._dealer_hand_value<=11:
            self.round._dealer_hand.append(PlayingCard(11,'SA'))
            self.round._dealer_hand_value+=11
        test = self.round._dealer_hand_value+11
        self.round.stay()
        self.assertEqual(test-10, self.round._dealer_hand_value)
    
    def test_function_count_payout_gives_back_the_bet_when_both_have_blackjack(self):
        self.round.new_round(25)
        self.round._dealer_hand = [PlayingCard(11,'SA'), PlayingCard(10,'SJ')]
        self.round._dealer_hand_value = 21
        self.round._player_hand = [PlayingCard(11,'SA'), PlayingCard(10,'SJ')]
        self.round._player_hand_value = 21
        self.round.count_payout()
        self.assertEqual(100, self.round._player.credits())

    def test_function_check_winner_returns_1_when_both_hand_value_21(self):
        self.round.new_round(25)
        self.round._dealer_hand_value = 21
        self.round._player_hand_value = 21
        test = self.round.check_winner()
        self.assertEqual(test, 1)
    
    def test_function_check_winner_returns_0_when_dealer_hand_value_is_higher(self):
        self.round.new_round(25)
        self.round._dealer_hand_value = 21
        self.round._player_hand_value = 20
        test = self.round.check_winner()
        self.assertEqual(test, 0)