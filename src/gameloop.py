import pygame
from blackjack import Player, Deck, Round
from board import Board


class GameLoop:
    def __init__(self, board: Board, renderer, event_queue, clock):
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._state = 0
        self._player = Player()
        self._round = Round(self._player, Deck())
        self._bet = 5

    def start(self):
        while True:
            if self._handle_events() is False:
                break
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        for event in self._event_queue.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.arrowkey_actions(1)
                if event.key == pygame.K_DOWN:
                    self.arrowkey_actions(3)
                if event.key == pygame.K_n:
                    self.n_button_actions()
                if event.key == pygame.K_SPACE:
                    self.spacebar_actions()
                if event.key == pygame.K_r:
                    return self.r_button_actions()
                if event.key == pygame.K_s:
                    self.s_button_actions()
            if event.type == pygame.QUIT:
                return False

    def _render(self):
        self._renderer.render()

    def switch_state(self, next_state: int):
        self._state = next_state

    def spacebar_actions(self):
        if self._state==1:
            self._round.new_round(self._bet)
            self._bet = 5
            self.switch_state(2)
            self._board.game_update(self._player.credits(
            ), self._round.player_hand(), self._round.dealer_hand(), 0)
        elif self._state==2:
            self._round.hit()
            self._board.game_update(self._player.credits(
            ), self._round.player_hand(), self._round.dealer_hand(), 0)
            if self._round.player_hand()[1] > 21:
                self._board.bust_out(self._player.credits())
                self.switch_state(4)
        elif self._state==3:
            result = self._round.dealer_deal()
            self._board.game_update(self._player.credits(
            ), self._round.player_hand(), self._round.dealer_hand(), 1)
            if result==1:
                self._board.round_end(self._player.credits(), True)
                self.switch_state(4)
            elif result==0:
                self._board.round_end(self._player.credits(), False)
                self.switch_state(4)
        elif self._state==4 and self._player.credits() >= 5:
            self.switch_state(1)
            self._board.place_bet(5, self._player.credits())

    def n_button_actions(self):
        if self._state==0:
            self.switch_state(1)
            self._board.start_game()
            self._board.place_bet(self._bet, self._player.credits())
        elif self._state==4 and self._player.credits() < 5:
            self.switch_state(1)
            self._player.reset()
            self._board.start_game()
            self._board.place_bet(self._bet, self._player.credits())

    def s_button_actions(self):
        if self._state==2:
            self._round.stay()
            self._board.game_update(self._player.credits(
            ), self._round.player_hand(), self._round.dealer_hand(), 1)
            self.switch_state(3)

    def r_button_actions(self):
        if self._state==4:
            return False
        return True

    def arrowkey_actions(self,direction):
        if self._state==1:
            if direction==1 and self._bet+5 <= self._player.credits(): #0=left,1=up,2=right,3=down
                self._board.place_bet(self._bet+5, self._player.credits())
                self._bet += 5
            elif direction==3 and self._bet-5 >= 5:
                self._board.place_bet(self._bet-5, self._player.credits())
                self._bet -= 5
