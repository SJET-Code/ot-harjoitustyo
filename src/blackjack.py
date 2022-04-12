import random


class Player:
    def __init__(self):
        self._credits = 100

    def bet(self, bet: int):
        if self._credits-bet >= 0:
            self._credits -= bet
            return True
        return False

    def payout(self, payout: int):
        self._credits += payout

    def credits(self):
        return self._credits

    def reset(self):
        self._credits = 100


class PlayingCard:
    def __init__(self, value: int, crest: str):
        self._value = value
        self._crest = crest

    def value(self):
        return self._value

    def crest(self):
        return self._crest

    def ace_change(self):
        if self._value == 11:
            self._value = 1

class Deck:
    def __init__(self):
        self._deck = self.create_deck()
        self._size = len(self._deck)

    def shuffle(self):
        self._deck = self.create_deck()
        random.shuffle(self._deck)
        self._size = len(self._deck)

    def get_card(self):
        card = self._deck.pop()
        self._size = len(self._deck)
        if self._size < 13:
            self.shuffle()
        return card

    def create_deck(self):
        crests = ['S', 'C', 'D', 'H']
        deck = []
        for crest in crests:
            for i in range(2, 15):
                if i == 11:
                    deck.append(PlayingCard(10, crest+'J'))
                elif i == 12:
                    deck.append(PlayingCard(10, crest+'Q'))
                elif i == 13:
                    deck.append(PlayingCard(10, crest+'K'))
                elif i == 14:
                    deck.append(PlayingCard(11, crest+'A'))
                else:
                    deck.append(PlayingCard(i, crest+str(i)))
        random.shuffle(deck)
        return deck.copy()


class Round:
    def __init__(self, player: Player, deck: Deck):
        self._player = player
        self._deck = deck
        self._dealer_hand = []
        self._player_hand = []
        self._dealer_hand_value = 0
        self._player_hand_value = 0
        self._bet = 5
        self._dealer_card=None

    def new_round(self, bet: int):
        self.reset()
        self._player.bet(bet)
        self._bet = bet
        card = self._deck.get_card()
        self._dealer_hand.append(card)
        self._dealer_hand_value += card.value()
        self._dealer_card = self._deck.get_card()
        card = self._deck.get_card()
        self._player_hand.append(card)
        self._player_hand_value += card.value()

    def hit(self):
        card = self._deck.get_card()
        self._player_hand_value += card.value()
        self._player_hand.append(card)
        if self._player_hand_value > 21:
            for player_card in self._player_hand:
                if player_card.value() == 11:
                    player_card.ace_change()
                    self._player_hand_value -= 10
                    break

    def stay(self):
        self._dealer_hand_value += self._dealer_card.value()
        self._dealer_hand.append(self._dealer_card)

    def dealer_deal(self):
        if self._dealer_hand_value >= 17:
            return self.check_winner()
        card = self._deck.get_card()
        self._dealer_hand_value += card.value()
        self._dealer_hand.append(card)
        if 17 <= self._dealer_hand_value <= 21:
            return self.check_winner()
        if self._dealer_hand_value > 21:
            self.check_for_aces(self._dealer_hand,self._dealer_hand_value)
            if self._dealer_hand_value >= 17:
                return self.check_winner()
        return 2


    def count_payout(self):
        if self._player_hand_value==21!=self._dealer_hand_value and len(self._player_hand)==2:
            payout = int(self._bet+self._bet*3/2)
            self._player.payout(payout)
        elif self._player_hand_value==21==self._dealer_hand_value:
            if len(self._player_hand)==2==len(self._dealer_hand):
                self._player.payout(self._bet)
        else:
            payout = self._bet*2
            self._player.payout(payout)

    def reset(self):
        self._dealer_hand = []
        self._player_hand = []
        self._dealer_hand_value = 0
        self._player_hand_value = 0

    def check_winner(self):
        if self._dealer_hand_value > 21:
            self.count_payout()
            return 1
        if self._dealer_hand_value == 21 == self._player_hand_value:
            self.count_payout()
            return 1
        if self._dealer_hand_value >= self._player_hand_value:
            return 0
        self.count_payout()
        return 1

    def player_hand(self):
        return self._player_hand, self._player_hand_value

    def dealer_hand(self):
        return self._dealer_hand, self._dealer_hand_value

    def check_for_aces(self, hand, hand_value):
        for card in hand:
            if card.value()==11:
                card.ace_change()
                hand_value-=10
                break
