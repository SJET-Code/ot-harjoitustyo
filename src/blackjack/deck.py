import random
from blackjack.playing_card import PlayingCard

class Deck:
    """Korttipakkaa kuvaava luokka, sisältää Pelikortti olioita listassa.
    """
    def __init__(self):
        """Uuden satunnaisen korttipakan luova konstruktori.
        Määrittelee myös korttipakan kooksi 52.

        """
        self._deck = self._create_deck()
        self._size = len(self._deck)

    def get_card(self):
        """Nostaa kortin pakasta, ja luo uuden sekoitetun pakan,
        jos pakassa on vähemmän kuin 13 korttia.

        Returns:
            PlayingCard : korttipakan päälimmäisin kortti
        """
        if self._size < 13:
            self._deck = self._create_deck()
            self._size = len(self._deck)
        card = self._deck.pop()
        self._size = len(self._deck)
        return card

    def _create_deck(self):
        """Luo uuden satunnaisen korttipakan.

        Returns:
            list : kopio luodusta korttipakasta.
        """
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
