class Player:
    """Pelaaja luokka, käsittelee pelaajan crediittejä.

    """
    def __init__(self):
        """Konstrurktori, mikä asettaa pelaajan aloitus crediiteiksi 100
        """
        self._credits = 100

    def bet(self, bet: int):
        """Vähentää pelaajan crediitejä panoksen verran.
        Jos panos on suurempi kuin pelaajan crediitit, ei crediittejä vähennetä.

        Args:
            bet (int): Pelaajan määrittelemä panos.

        Returns:
            bool : True, jos pelaajalla on tarpeeksi crediittejä, muuten False.
        """
        if self._credits-bet >= 0:
            self._credits -= bet
            return True
        return False

    def payout(self, payout: int):
        """Kasvattaa pelaajan crediittejä voitetulla summalla.

        Args:
            payout (int): Pelaajan voittama määrä crediittejä.
        """
        self._credits += payout

    def credits(self):
        """Funktio, jolla saadaan tieto pelaajan crediiteistä muille osille ohjelmaa.

        Returns:
            int : Pelaajan crediitit.
        """
        return self._credits

    def reset(self):
        """Funktio, joka asettaa pelaajan crediitit takaisin aloitus asemaan uutta peliä varten.

        """
        self._credits = 100
