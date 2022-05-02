import pygame


class Renderer:
    """Peliruudun piirtävä luokka.

    Attributes:
        display: pygame display olio, mikä on alustettu index.py tiedostossa.
        board: Board-olio, joka käsittelee kuvien asettelua.
    """
    def __init__(self, display, board):
        """Atribuutit alustava konstruktori.

        Args:
            display (pygame.display): pygame display olio, mikä on alustettu index.py tiedostossa.
            board (Board): Board-olio, joka käsittelee kuvien asettelua.
        """
        self._display = display
        self._board = board

    def render(self):
        """Piirtää pelitilanteen mukaan kuvat ruudulle.
        """
        if self._board.state['game']:
            self._display.fill((46, 125, 50, 1))
            self._board.sprites['game_sprites'].draw(self._display)
            self._board.sprites['temp_game_sprites'].draw(self._display)
        elif self._board.state['start']:
            self._display.fill((46, 125, 50, 1))
            self._board.sprites['end_sprites'].draw(self._display)
            self._board.sprites['start_sprites'].draw(self._display)
        elif self._board.state['end']:
            self._display.fill((46, 125, 50, 1))
            self._board.sprites['end_sprites'].draw(self._display)
            self._board.sprites['temp_end_sprites'].draw(self._display)
        pygame.display.update()
