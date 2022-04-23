import pygame


class Renderer:
    def __init__(self, display, board):
        self._display = display
        self._board = board

    def render(self):
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
