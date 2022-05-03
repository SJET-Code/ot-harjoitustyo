import pygame
from blackjack.player import Player
from blackjack.deck import Deck
from blackjack.round import Round
from ui.board import Board
from string import ascii_letters


class GameLoop:
    """Pelin silmukka, jonka avulla saadan käyttöliittymästä pelaajan komennot,
    ja välitetään ne pelilogiikalle, ja muille käyttöliittymän osille.

    Attributes:
        board: Board-olio, joka on vastuussa kuvien asettelusta ruudulle.
        renderer: Renderer-olio, joka on vastuussa ruudun piirtämisestä.
        event_queue: EventQueue-olio, joka on vastuussa pelaajan näppäinkomentojen poiminnasta.
        clock: Clock-olio, joka on vastuussa pelin piirtonopeudesta.
    """
    def __init__(self, board: Board, renderer, event_queue, clock):
        """Alustaa sisäiset muuttujat ja työkalut.

        Args:
            board (Board): Board-olio, joka on vastuussa kuvien asettelusta ruudulle.
            renderer (_type_): Renderer-olio, joka on vastuussa ruudun piirtämisestä.
            event_queue (_type_): EventQueue-olio, joka on vastuussa pelaajan näppäinkomentojen poiminnasta.
            clock (_type_): Clock-olio, joka on vastuussa pelin piirtonopeudesta.
        """
        self._loop_tools = {
            'renderer' : renderer,
            'event_queue' : event_queue,
            'clock' : clock
        }
        self._game_tools = {
            'player' : None,
            'round' : Round(Player(), Deck()),
            'bet' : 5,
            'name' : "",
            'state' : 0
        }
        self._game_tools['player'] = self._game_tools['round'].player()
        self._board = board

    def start(self):
        """Aloittaa pelisilmukan.
        """
        while True:
            if self._handle_events() is False:
                break
            self._render()
            self._loop_tools['clock'].tick(60)

    def _handle_events(self):
        """Käsittelee pelaajan näppäinsyötteet ja vie ne eteenpäin muille funktioille.

        Returns:
            bool : False jos pelaaja sulkee ikkunan, muuten True.
        """
        for event in self._loop_tools['event_queue'].get():
            if event.type == pygame.KEYDOWN and self._game_tools['state'] != 5:
                if event.key == pygame.K_UP:
                    self._arrowkey_actions(1)
                if event.key == pygame.K_DOWN:
                    self._arrowkey_actions(3)
                if event.key == pygame.K_n:
                    self._n_button_actions()
                if event.key == pygame.K_SPACE:
                    self._spacebar_actions()
                if event.key == pygame.K_RETURN:
                    self._return_button_actions()
                if event.key == pygame.K_r:
                    return self._r_button_actions()
                if event.key == pygame.K_s:
                    self._s_button_actions()
                if event.key == pygame.K_d:
                    self._d_button_actions()
                return True

            if event.type == pygame.KEYDOWN and self._game_tools['state'] == 5:
                self._handle_user_input(event.key, event.unicode)
                return True

            if event.type == pygame.QUIT:
                return False
        return True

    def _handle_user_input(self, key, letter):
        """Tulkitsee pelaajan nimimerkki syötteen pistetulosta varten.

        Args:
            key (pygame.K_): pygame näppäin koodi.
            letter (str): unicode kirjain.

        Returns:
            bool : True aina.
        """
        if key == pygame.K_BACKSPACE:
            self._game_tools['name'] = self._game_tools['name'][:-1]
            self._board.user_input(self._game_tools['name'])
        elif key == pygame.K_RETURN and len(self._game_tools['name']) == 3:
            self._board.confirm_user_input()
            self._game_tools['round'].reset()
            self._switch_state(0)
            self._game_tools['name'] = ""
        elif len(self._game_tools['name']) < 3 and letter in ascii_letters:
            self._game_tools['name'] += letter
            self._board.user_input(self._game_tools['name'])
        return True

    def _render(self):
        """Kutsuu ruudunpiirto funktiota.
        """
        self._loop_tools['renderer'].render()

    def _switch_state(self, next_state: int):
        """Vaihtaa peli vaiheen, 0 on pelin aloitusruutu, 1 on panosten asetus,
        2 on pelaajan käsien toimintojen valinnat, 3 on jakajan korttien käsittely,
        4 on kierroksen loppu ja 5 on korkeimmat pisteet näkymä ja pelaajan tuloksen tallennus.

        Args:
            next_state (int): Pelin seuraava vaihe.
        """
        self._game_tools['state'] = next_state

    def _spacebar_actions(self):
        """Käsittelee väli näppäimen toiminnot.
        """
        if self._game_tools['state'] == 2:
            if self._game_tools['round'].hit():
                if self._game_tools['round'].check_bust():
                    self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                    self._board.game_update(self._game_tools['player'].credits(
                    ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 1)
                    self._board.round_end(self._game_tools['player'].credits())
                    self._switch_state(4)
                else:
                    self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                    self._switch_state(3)
                    self._board.game_update(self._game_tools['player'].credits(
                    ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 1)
            else:
                self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)
                if self._game_tools['round'].check_bust():
                    self._board.round_end(self._game_tools['player'].credits())
                    self._switch_state(4)
                self._check_special_hand_options()
        elif self._game_tools['state'] == 3:
            if self._game_tools['round'].dealer_deal():
                self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 1)
                self._board.round_end(self._game_tools['player'].credits())
                self._switch_state(4)
            else:
                self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 1)
        elif self._game_tools['state'] == 4 and self._game_tools['player'].credits() >= 5:
            self._game_tools['round'].reset()
            self._switch_state(1)
            self._board.place_bet(5, self._game_tools['player'].credits(),
            self._game_tools['round'].player_hands())

    def _return_button_actions(self):
        """Käsittelee rivinvaihto näppäimen toiminnot.
        """
        if self._game_tools['state'] == 1:
            self._player_hands_handler()
        elif self._game_tools['state'] == 2 and self._game_tools['round'].check_split():
            self._game_tools['round'].split()
            self._board.set_active_hand(self._game_tools['round'].check_active_hand())
            self._board.game_update(self._game_tools['player'].credits(
            ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)

    def _n_button_actions(self):
        """Käsittelee n näppäimen toiminnot.
        """
        if self._game_tools['state']==0:
            self._switch_state(1)
            self._game_tools['player'].reset()
            self._board.start_game()
            self._board.place_bet(self._game_tools['bet'], self._game_tools['player'].credits(),
            self._game_tools['round'].player_hands())
        elif self._game_tools['state']==4 and self._game_tools['player'].credits() < 5:
            self._switch_state(1)
            self._game_tools['player'].reset()
            self._game_tools['round'].reset()
            self._board.start_game()
            self._board.place_bet(self._game_tools['bet'], self._game_tools['player'].credits(),
            self._game_tools['round'].player_hands())

    def _s_button_actions(self):
        """Käsittelee s näppäimen toiminnot.
        """
        if self._game_tools['state'] == 1 and 0 < len(self._game_tools['round'].player_hands()) < 3:
            self._game_tools['round'].new_round_deal()
            self._game_tools['bet'] = 5
            self._switch_state(2)
            self._board.game_update(self._game_tools['player'].credits(
            ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)
            self._check_special_hand_options()
        elif self._game_tools['state'] == 2:
            if self._game_tools['round'].stay():
                self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                self._switch_state(3)
                self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 1)
            else:
                self._board.set_active_hand(self._game_tools['round'].check_active_hand())
                self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)
            self._check_special_hand_options()
            

    def _r_button_actions(self):
        """Käsittelee r näppäimen toiminnot.
        """
        if self._game_tools['state'] == 2 and self._game_tools['round'].check_surrender():
            self._game_tools['round'].surrender_hand()
            self._board.set_active_hand(self._game_tools['round'].check_active_hand())
            self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)
        if self._game_tools['state'] == 4:
            self._board.end_game(self._game_tools['player'].credits())
            self._switch_state(5)

    def _d_button_actions(self):
        """Käsittelee d näppäimen toiminnot.
        """
        if self._game_tools['state'] == 2 and self._game_tools['round'].check_double_down():
            self._game_tools['round'].double_down()
            self._board.game_update(self._game_tools['player'].credits(
                ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)

    def _arrowkey_actions(self, direction):
        """Käsittelee nuoli näppäinten toiminnot.

        Args:
            direction (int): Suunta, 0 = left, 1 = up, 2 = right, 3 = down.
        """
        if self._game_tools['state']==1:
            if direction==1 and self._game_tools['bet']+5 <= self._game_tools['player'].credits():
                self._board.place_bet(self._game_tools['bet']+5, self._game_tools['player'].credits(),
                self._game_tools['round'].player_hands())
                self._game_tools['bet'] += 5
            elif direction==3 and self._game_tools['bet']-5 >= 5:
                self._board.place_bet(self._game_tools['bet']-5, self._game_tools['player'].credits(),
                self._game_tools['round'].player_hands())
                self._game_tools['bet'] -= 5

    def _player_hands_handler(self):
        """Käsittelee pelaajan käsien määrän valinnan rivinvaihto näppäimen kautta.
        """
        if len(self._game_tools['round'].player_hands()) < 3 and self._game_tools['player'].credits() >= self._game_tools['bet']:
            self._game_tools['round'].add_player_hand(self._game_tools['bet'])
            self._game_tools['bet'] = 5
            self._board.place_bet(self._game_tools['bet'], self._game_tools['player'].credits(),
            self._game_tools['round'].player_hands())
        else:
            self._game_tools['round'].new_round_deal()
            self._game_tools['bet'] = 5
            self._switch_state(2)
            self._board.set_active_hand(self._game_tools['round'].check_active_hand())
            self._board.game_update(self._game_tools['player'].credits(
            ), self._game_tools['round'].player_hands(), self._game_tools['round'].dealer_hand(), 0)
            self._check_special_hand_options()

    def _check_special_hand_options(self):
        """Tarkistaa, onko pelattavalla kädellä mahdollisuutta jakaa, antautua tai tuplata.
        """
        self._board.set_active_hand(self._game_tools['round'].check_active_hand())
        if self._game_tools['round'].check_split():
            self._board.show_split_option()
        if self._game_tools['round'].check_surrender():
            self._board.show_surrender_option()
        if self._game_tools['round'].check_double_down():
            self._board.show_double_down_option()


        