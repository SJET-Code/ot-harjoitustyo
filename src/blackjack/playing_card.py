class PlayingCard:
    """Pelikorttia kuvaava luokka.
    """
    def __init__(self, value: int, crest: str):
        """Konstruktori, joka määrittää kortin tiedot.

        Args:
            value (int): Kortin arvo (1-11).
            crest (str): Kortin maa (S, C, D tai H).
        """
        self._value = value
        self._crest = crest

    def value(self):
        """Funktio, joka antaa tiedon kortin arvosta ohjelman muille osille.

        Returns:
            int : Kortin arvo (1-11).
        """
        return self._value

    def crest(self):
        """Funktio, joka antaa tiedon kortin maasta ohjelman muille osille.

        Returns:
            str : Kortin maa (S, C, D tai H).
        """
        return self._crest

    def ace_change(self):
        """Suorittaa ässille ominaisen arvon vaihdon, arvosta 11 arvoon 1,
        tarkastaen ensin, että kyseessä on kortti, jonka arvo on 11.
        """
        if self._value == 11:
            self._value = 1
