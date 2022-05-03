import numpy as np
from blackjack.player import Player
from blackjack.playing_card import PlayingCard

class Hand:
    """Yhtä pelaajan kättä, eli kortti yhdistelmää kuvaava luokka.

    Attributes:
        bet: Kädelle asetettu aloituspanos.
        player: Viite crediiteistä huolehtivaan Pelaaja-olioon.
    """
    def __init__(self, bet:int, player:Player):
        """Luokan konstruktori, joka alustaa atribuutit, ja vähentää
        panoksen pelaajan crediiteistä.

        Args:
            bet (int): Pelaajan kädelle asettama alkupanos.
            player (Player): Viite Pelaaja-olioon.
        """
        self._bet = bet
        self._player = player
        self._attributes = {
            'cards' : [],
            'value' : 0,
            'stay' : False,
            'bust' : False,
            'surrender' : False,
            'can_split' : False,
            'double_down' : False,
            'win' : False,
            'win_message' : ""
        }
        self._player.bet(bet)

    def add_card(self, new_card:PlayingCard):
        """Lisää kortin käteen, kun pelaaja valitsee 'hit',
        ja tarkistaa käden arvon lisäyksen jälkeen, tehden tarvittavat
        toimenpiteet, jos käden arvo ylittää arvon 21 tai jos pelaaja
        oli aikaisemmin valinnut tuplaus vaihtoehdon.

        Args:
            new_card (PlayingCard): Käteen lisättävä kortti.
        """
        if self._attributes['value'] > 21:
            for card in self._attributes['cards']:
                if card.value() == 11:
                    card.ace_change()
                    self._attributes['value'] -= 10
                    break
        self._attributes['can_split'] = False
        self._attributes['value'] += new_card.value()
        self._attributes['cards'].append(new_card)
        if self._attributes['value'] > 21:
            for card in self._attributes['cards']:
                if card.value() == 11:
                    card.ace_change()
                    self._attributes['value'] -= 10
                    break
        if self._attributes['value'] > 21:
            self._attributes['bust'] = True
        if self._attributes['double_down']:
            self._attributes['stay'] = True

    def starting_deal(self, card1:PlayingCard, card2:PlayingCard):
        """Lisää käteen kierroksen aloittavat 2 korttia, ja tarkistaa onko
        käden jako mahdollista.

        Args:
            card1 (PlayingCard): Ensimmäinen lisättävä kortti.
            card2 (PlayingCard): Toinen lisättävä kortti.
        """
        if card1.value() == card2.value() and self._player.credits() >= self._bet:
            self._attributes['can_split'] = True
        self._attributes['value'] = card1.value() + card2.value()
        self._attributes['cards'].append(card1)
        self._attributes['cards'].append(card2)

    def split(self):
        """Suorittaa käden jakamisen.

        Returns:
            Hand(): Uusi Hand-olio
        """
        self._attributes['can_split'] = False
        split_card = self._attributes['cards'].pop()
        self._attributes['value'] -= split_card.value()
        new_hand = Hand(self._bet, self._player)
        new_hand.add_card(split_card)
        return new_hand

    def double_down(self):
        """Suorittaa käden tuplauksen.

        Returns:
            bool : True jos tuplaus onnistui, muuten False
        """
        if self._player.credits() >= self._bet:
            self._player.bet(self._bet)
            self._bet = self._bet*2
            self._attributes['double_down'] = True
            return True
        return False

    def stand(self):
        """Kuvaa pelaajan valintaa 'stay', eli nostettuihin kortteihin jäämistä.
        """
        self._attributes['stay'] = True

    def payout(self, dealer_hand : list, dealer_hand_value : int):
        """Tarkistaa voittiko pelaajan käsi jakajan, ja jos voitti
        niin millä tavalla, maksaen myös pelaajalle voitto summan crediittejä.

        Args:
            dealer_hand (list): Jakajan kortit.
            dealer_hand_value (int): Jakajan korttien yhteisarvo.
        """
        self._attributes['win'] = True
        if self._attributes['value'] == 21 and len(self._attributes['cards']) == 2:
            self._blackjack_payout(dealer_hand, dealer_hand_value)
        elif dealer_hand_value > 21:
            payout = self._bet * 2
            self._player.payout(payout)
            self._attributes['win_message'] = f'Dealer busts out! Won {payout}!'
        elif self._attributes['value'] > dealer_hand_value:
            payout = self._bet * 2
            self._player.payout(payout)
            self._attributes['win_message'] = f'Point win! Won {payout}!'
        else:
            self._attributes['win_message'] = f'Dealer win! Lost {self._bet}!'

    def _blackjack_payout(self, dealer_hand : list, dealer_hand_value : int):
        """Käsittelee eri tavat miten potti voi jakaantua,
        kun pelaajalla on Blackjack.

        Args:
            dealer_hand (list): Jakajan kortit.
            dealer_hand_value (int): Jakajan korttien yhteisarvo.
        """
        if (self._attributes['value'] == 21 != dealer_hand_value and
        len(self._attributes['cards']) == 2):
            payout = int(np.ceil(self._bet + np.multiply(self._bet, 1.5)))
            self._player.payout(payout)
            self._attributes['win_message'] = f'Blackjack! Won {payout}!'
        elif (self._attributes['value'] == 21 == dealer_hand_value and
        len(self._attributes['cards']) == 2 != len(dealer_hand)):
            payout = int(np.ceil(self._bet + np.multiply(self._bet, 1.5)))
            self._player.payout(payout)
            self._attributes['win_message'] = f'Blackjack! Won {payout}!'
        elif (self._attributes['value'] == 21 == dealer_hand_value and
        len(self._attributes['cards']) == 2 == len(dealer_hand)):
            payout = self._bet
            self._player.payout(payout)
            self._attributes['win_message'] = f'Both have Blackjack! {payout} paid back!'

    def surrender_hand(self):
        """Suorittaa käden antautumis toimenpiteen, eli antaa pelaajalle puolet
        panoksestaan takaisin, mahdollinen vain kahden ensimmäisen kortin jälkeen.
        """
        if len(self._attributes['cards']) == 2:
            self._attributes['surrender'] = True
            self._player.payout(self._bet//2)

    def stay(self):
        """Palauttaa tiedon, onko käsi jäänyt nykyisiin kortteihin.

        Returns:
            bool : True jos käsi on jäänyt nykyisiin kortteihin, muuten False
        """
        return self._attributes['stay']

    def cards(self):
        """Palauttaa listan kaikista käden korteista.

        Returns:
            list : Lista käden korteista.
        """
        return self._attributes['cards']

    def value(self):
        """Paluttaa käden korttien yhteisarvon.

        Returns:
            int : Käden korttien yhteisarvo.
        """
        return self._attributes['value']

    def bust(self):
        """Palauttaa tiedon, onko käden yhteisarvo ylittänyt arvon 21.

        Returns:
            bool : True jos käden yhteisarvo > 21, muuten False.
        """
        return self._attributes['bust']

    def surrender(self):
        """Palauttaa tiedon, onko käsi antautunut.

        Returns:
            bool : True jos käsi on antautunut, muuten False.
        """
        return self._attributes['surrender']

    def can_split(self):
        """Palauttaa tiedon, onko käden jakaminen mahdollista.

        Returns:
            bool : True jos käden jakaminen on mahdollista, muuten False.
        """
        return self._attributes['can_split']

    def bet(self):
        """Palauttaa tiedon käden panoksesta.

        Returns:
            int: Käden panos.
        """
        return self._bet

    def win(self):
        """Palauttaa tiedon, onko käsi käsitelty funktiossa payout.

        Returns:
            bool : True jos käsitelty, muuten False.
        """
        return self._attributes['win']

    def win_message(self):
        """Palauttaa tiedon käden lopputuloksesta.

        Returns:
            str: Käden lopputulos, mikä näytetään pelaajalle kierroksen lopussa.
        """
        return self._attributes['win_message']
