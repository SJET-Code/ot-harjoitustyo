from blackjack.player import Player
from blackjack.deck import Deck
from blackjack.hand import Hand

class Round:
    """Blackjack kierrosta simuloiva luokka.
    """
    def __init__(self, player: Player, deck: Deck):
        """Luokan alustava konstruktori, asettaa luokan sisäiset muuttajat oletuisarvoiksi.

        Args:
            player (Player): pelaajaa kuvaava luokka.
            deck (Deck): korttipakkaa kuvaava luokka.
        """
        self._player = player
        self._deck = deck
        self._dealer_hand = []
        self._player_hands = []
        self._dealer_hand_value = 0
        self._dealer_card = None

    def add_player_hand(self, bet: int):
        """Lisää uuden pelattavan käden pelaajalle.

        Args:
            bet (int): pelaajan panos tälle kädelle.
        """
        self._player_hands.append(Hand(bet, self._player))

    def new_round_deal(self):
        """Jakaa kierroksen aloittavat kortit, eli kaksi korttia pelaajan käsille,
        ja kaksi korttia jakajalle, joista toinen on kuvapuoli alaspäin.
        """
        for hand in self._player_hands:
            card1 = self._deck.get_card()
            card2 = self._deck.get_card()
            hand.starting_deal(card1, card2)
        card = self._deck.get_card()
        self._dealer_hand.append(card)
        self._dealer_hand_value += card.value()
        self._dealer_card = self._deck.get_card()

    def hit(self):
        """Nostaa aktiiviseen käteen yhden kortin, jos kaikki kädet
        on käsitelty palautetaan tieto siitä.

        Returns:
            bool : True jos kaikki kädet on käsitelty, eli ei ole
            aktiivista kättä, muuten False.
        """
        hand = self.check_active_hand()
        if not hand:
            return True
        hand.add_card(self._deck.get_card())
        if not self.check_active_hand():
            return True
        return False

    def check_split(self):
        """Tarkistaa voiko aktiivisen käden jakaa, ja onko käsiä yli 4.
        Pelissä on rajana maksimissaan 5 kättä per kierros.

        Returns:
            bool : True jos aktiivine käsi on jaettavissa, muuten False.
        """
        if len(self._player_hands) > 4:
            return False
        hand = self.check_active_hand()
        if not hand:
            return False
        if hand.can_split():
            return True
        return False

    def split(self):
        """Jakaa aktiivisen käden toisen kortin uudeksi kädeksi.
        """
        hand = self.check_active_hand()
        if not hand:
            pass
        else:
            new_hand = hand.split()
            self._player_hands.append(new_hand)

    def stay(self):
        """Välittää aktiiviselle kädelle tiedon, että pelaaja haluaa jäädä
        nykyisiin kortteihin.

        Returns:
            bool : True jos kaikki kädet on käsitelty, eli ei ole
            aktiivista kättä, muuten False.
        """
        hand = self.check_active_hand()
        if not hand:
            return True
        hand.stand()
        if not self.check_active_hand():
            return True
        return False

    def dealer_deal(self):
        """Nostaa jakajalle lisää kortteja, kun kaikki pelaajan kädet on käsitelty.
        Käsittelee jakajan käden arvoa, ja antaa tiedon onko käsi loppuunkäsitelty vai ei.

        Returns:
            bool : True jos jakajan käsi on loppuunkäsitelty (arvo > 16), muuten False.
        """
        if len(self._dealer_hand) == 1:
            self._dealer_hand_value += self._dealer_card.value()
            self._dealer_hand.append(self._dealer_card)
        if self._dealer_hand_value > 21:
            self._check_for_aces()
        if self._dealer_hand_value > 16:
            return self.payout_hands()
        card = self._deck.get_card()
        self._dealer_hand_value += card.value()
        self._dealer_hand.append(card)
        if self._dealer_hand_value > 21:
            self._check_for_aces()
        if self._dealer_hand_value > 16:
            return self.payout_hands()
        return False

    def check_bust(self):
        """Tarkistaa ovatko kaikki pelaajan kädet poissa pelistä.

        Returns:
            bool : True jos kaikki pelaajan kädet ovat hävinneet, muuten False.
        """
        bust = True
        for hand in self._player_hands:
            if hand.bust() or hand.surrender():
                continue
            bust = False
        return bust

    def payout_hands(self):
        """Käsittelee kaikki pelaajan ei hävinneet kädet, ja ohjaa ne voiton tarkastukseen.

        Returns:
            bool : True kun kaikki kädet on käsitelty.
        """
        for hand in self._player_hands:
            if hand.bust() or hand.surrender():
                continue
            hand.payout(self.dealer_hand()[0], self.dealer_hand()[1])
        return True

    def reset(self):
        """Palauttaa oletusarvot  pelaajan ja jakajan käsille.
        """
        self._dealer_hand = []
        self._player_hands = []
        self._dealer_hand_value = 0
        self._dealer_card = None

    def player_hands(self):
        """Palauttaa pelaajan kädet listana.

        Returns:
            list : Lista Hand-olioita, jotka kuvaavat pelaajan käsiä.
        """
        return self._player_hands

    def dealer_hand(self):
        """Palauttaa jakajan käden, ja käden arvon.

        Returns:
            tuple : Ensimmäisessä indeksissä lista jakajan korteista,
            toisessa indeksissä jakajan korttien yhteissumma
        """
        return self._dealer_hand, self._dealer_hand_value

    def _check_for_aces(self):
        """Tarkistaa jakajan käden ässä tilanteen, ja muuttaa ensimmäisen
        löydetyn ässän arvon yhdestätoista yhteen.
        """
        for card in self._dealer_hand:
            if card.value() == 11:
                card.ace_change()
                self._dealer_hand_value -= 10
                break

    def surrender_hand(self):
        """Suorittaa antautumis operaation aktiiviselle kädelle.
        """
        hand = self.check_active_hand()
        if not hand:
            return
        if len(hand.cards()) == 2:
            hand.surrender_hand()

    def check_surrender(self):
        """Tarkistaa voiko aktiivinen käsi antautua.

        Returns:
            bool : True jos aktiivinen käsi voi antautua, muuten False.
        """
        hand = self.check_active_hand()
        if not hand:
            return False
        if len(hand.cards()) == 2:
            return True
        return False

    def check_double_down(self):
        """Tarkistaa voiko aktiivinen käsi tuplata.

        Returns:
            bool : True jos aktiivinen käsi voi tuplata, muuten False.
        """
        hand = self.check_active_hand()
        if not hand:
            return False
        if len(hand.cards()) == 2 and self._player.credits() >= hand.bet():
            return True
        return False

    def double_down(self):
        """Suorittaa tuplaus operaation aktiiviselle kädelle.
        """
        hand = self.check_active_hand()
        if not hand:
            return
        if len(hand.cards()) == 2 and self._player.credits() >= hand.bet():
            hand.double_down()

    def check_active_hand(self):
        """Palauttaa aktiivisen käden.

        Returns:
            Hand : Peli vuorossa oleva käsi.
        """
        for hand in self._player_hands:
            if hand.bust() or hand.surrender() or hand.stay():
                continue
            return hand
        return None

    def player(self):
        """Palauttaa Pelaaja-olion.

        Returns:
            Player : Pelaaja-olio, joka huolehtii crediiteistä.
        """
        return self._player
