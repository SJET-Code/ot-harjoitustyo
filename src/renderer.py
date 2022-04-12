import pygame


class Renderer:
    def __init__(self, display, board):
        self._display = display
        self._board = board

    def render(self):
        if self._board.game:
            self._display.fill((46, 125, 50, 1))
            self._board.game_sprites.draw(self._display)
            self._board.temp_game_sprites.draw(self._display)
        elif self._board.start:
            self._board.start_sprites.draw(self._display)
        pygame.display.update()
