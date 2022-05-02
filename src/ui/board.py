import pygame
from ui.sprites.card import Card
from ui.sprites.card_back import CardBack
from ui.sprites.deck import DeckSprite
from ui.sprites.text import Text
from ui.sprites.button import Button
from repositories.score_repository import score_repository

class Board:
    """Pelielementtien ruudulle asettelusta vastaava luokka.
    """
    def __init__(self):
        """Sisäiset muuttujat alustava konstruktori. Sprites dictionary sisältää
        eri pelitilanteiden sprite oliot ja hetkelliset spritet. State dictionary
        sisältää tiedon pelin tilasta.
        """
        self.sprites = {
            'start_sprites' : pygame.sprite.Group(),
            'game_sprites' : pygame.sprite.Group(),
            'temp_game_sprites' : pygame.sprite.Group(),
            'end_sprites' : pygame.sprite.Group(),
            'temp_end_sprites' : pygame.sprite.Group()
        }
        self.player_name = ""
        self.score = 0
        self._active_hand = None
        self.state = {'start' : True, 'game' : False, 'end' : False}
        self._color = {
            'black' : (0,0,0),
            'white' : (255, 255, 255)
            }
        text = Text('New Game', 80, self._color['white'], 1330//2-200, 600)
        self.sprites['start_sprites'].add(
            text,
            Button(1330//2-200+text.width()+10, 630, 'n')
            )

    def game_update(self, player_credits: int, player_hands: list, dealer_cards: tuple, game_state: int):
        """Asettelee yleisen pelitilanteen elementit ja pelaajan ohjeistuksen.

        Args:
            player_credits (int): pelaajan crediitit.
            player_hands (list): pelaajan kaikki kädet sisältävä lista.
            dealer_cards (tuple): jakajan kortit, ja korttien yhteisarvo.
            game_state (int): 0 jos pelaajan käsiä vielä pelataan, muuten 1.
        """
        self.sprites['temp_game_sprites'].empty()
        if game_state == 0:
            self.hand_compiler(player_hands, dealer_cards)
            hit = Text('HIT', 50, self._color['white'], 600, 650)
            stay = Text('STAY', 50, self._color['white'], 300, 650)
            self.sprites['temp_game_sprites'].add(
                hit,
                Button(600+hit.width()+10, 660, 'space'),
                stay,
                Button(300+stay.width()+10, 660, 's'),
                Text(f'CREDITS: {player_credits}', 30, self._color['white'], 10, 650)
            )
        elif game_state == 1:
            self.hand_compiler(player_hands, dealer_cards)
            text = Text('NEXT CARD', 50, self._color['white'], 950, 100)
            self.sprites['temp_game_sprites'].add(
                Text(f'CREDITS: {player_credits}', 30, self._color['white'], 10, 650),
                text,
                Button(950+text.width()+10, 110, 'space')
                )

    def place_bet(self, bet: int, player_credits: int, player_hands:list):
        """Asettelee panoksen asetteluun liittyvät pelielementit.

        Args:
            bet (int): pelaajan valitsema panos.
            player_credits (int): pelaajan crediitit.
            player_hands (list): lista pelaajan käsistä tällä kierroksella.
        """
        self.sprites['temp_game_sprites'].empty()
        button1 = Button(10, 440, 'return')
        button2 = Button(1330//2-100, 650, 's')
        if len(player_hands) < 3:
            text = Text(f'BET FOR HAND #{len(player_hands)+1}: {bet}', 30, self._color['white'], 10, 550)
            self.sprites['temp_game_sprites'].add(
                text,
                Text(f'CREDITS: {player_credits-bet}', 30, self._color['white'], 10, 650),
                Button(text.width()+20, 530, 'arrows'),
                button1,
                Text('TO CONFIRM BET', 30, self._color['white'], button1.width()+20, 470),
                button2,
                Text('TO START THE ROUND', 30, self._color['white'], button2.width()+1330//2-100, 650)
                )
        else:
            self.sprites['temp_game_sprites'].add(
                Text(f'CREDITS: {player_credits}', 30, self._color['white'], 10, 650),
                button1,
                Text('TO START THE ROUND', 30, self._color['white'], button1.width()+20, 470)
                )
        for i in range(len(player_hands)):
            self.sprites['temp_game_sprites'].add(
                Text(f'HAND #{i+1}: BET: {player_hands[i].bet()}', 40, self._color['white'], 300 + i * 300, 300))

    def round_end(self, player_credits: int):
        """Asettelee kierroksen lopun elementit.

        Args:
            player_credits (int): pelaajan crediitit.
        """
        if player_credits >= 5:
            text1 = Text('Round Over! Press',
                     30, self._color['white'], 300, 670)
            button1 = Button(310 + text1.width(), 670, 'space')
            text2 = Text('for a new round and',
                     30, self._color['white'], 320 + button1.width() + text1.width(), 670)
            button2 = Button(330 + button1.width() + text2.width() + text1.width(), 670, 'r')
            text3 = Text('to retire',
                     30, self._color['white'], 340 + button1.width() + text2.width() +
                     button2.width() + text1.width(), 670)
            self.sprites['temp_game_sprites'].add(
                text1, text2, text3,
                button1, button2
                )
        else:
            text1 = Text('Round Over, You lost! Press',
                     30, self._color['white'], 300, 670)
            button1 = Button(310 + text1.width(), 670, 'n')
            text2 = Text('to start a new game',
                     30, self._color['white'], 320 + button1.width() + text1.width(), 670)
            self.sprites['temp_game_sprites'].add(
                text1, text2, button1)

    def start_game(self):
        """Muuttaa tilan peli tilaan.
        """
        self.state['start'] = False
        self.state['game'] = True
        self.sprites['game_sprites'].add(DeckSprite(0, 0))

    def end_game(self, score : int):
        """Muuttaa tilan loppu tilaan, ja asettelee pelaajan tuloksen.

        Args:
            score (int): pelaajan tulos.
        """
        self.state['game'] = False
        self.state['end'] = True
        self.score = score
        self.load_scoreboard()
        self.sprites['temp_end_sprites'].add(Text(f'Your score is {self.score} add a name:',
        30, self._color['white'], 350, 600)
        )

    def user_input(self, name:str):
        """Asettelee pelaajan nimimerkin valinnan.

        Args:
            name (str): pelaajan nimimerkki syöte.
        """
        self.player_name = name.upper()
        self.sprites['temp_end_sprites'].empty()
        text = Text(self.player_name, 50, self._color['white'], 720, 590)
        button = Button(720+text.width()+10, 570, 'return')
        self.sprites['temp_end_sprites'].add(
            text,
            button,
            Text(f'Your score is {self.score} add a name:', 30, self._color['white'], 350, 600),
            Text('to confirm', 30, self._color['white'], 720+text.width()+20+button.width(),600)
        )

    def show_split_option(self):
        """Asettelee ohjeistuksen jakamisen mahdollisuudesta.
        """
        text = Text('SPLIT', 50, self._color['white'], 900, 650)
        self.sprites['temp_game_sprites'].add(
            text,
            Button(900 + text.width(), 630, 'return')
        )

    def show_surrender_option(self):
        """Asettelee ohjeistuksen antautumisen mahdollisuudesta.
        """
        text = Text('SURRENDER', 30, self._color['white'], 5, 250)
        self.sprites['temp_game_sprites'].add(
            text,
            Button(50, 260 + text.height(), 'r')
        )
    
    def show_double_down_option(self):
        """Asettelee ohjeistuksen tuplauksen mahdollisuudesta.
        """
        text = Text('DOUBLE DOWN', 30, self._color['white'], 5, 500)
        self.sprites['temp_game_sprites'].add(
            text,
            Button(50, 510 + text.height(), 'd')
        )

    def load_scoreboard(self):
        """Asettelee highscoret, eli korkeimmat pistetulokset.
        """
        self.sprites['end_sprites'].empty()
        scores = score_repository.get_scores()
        self.sprites['end_sprites'].add(
            Text('Highscores:', 50, self._color['white'], 530, 10))
        y_position = 100
        place = 1
        for row in scores:
            self.sprites['end_sprites'].add(
                Text(f"{place}. {row['player']}", 30, self._color['white'], 455, y_position),
                Text(f"SCORE: {row['score']}", 30, self._color['white'], 755, y_position)
            )
            place += 1
            y_position += 40

    def confirm_user_input(self):
        """Lisää pelaajan tuloksen tietokantaan, ja asettelee highscoret uudestaan.
        """
        score_repository.add_score(self.player_name, self.score)
        self.sprites['temp_end_sprites'].empty()
        self.load_scoreboard()
        self.state['end'] = False
        self.state['start'] = True
        self.player_name = ""

    def _card_compiler(self, cards:list, user:int, hand_number:int, message:str, active:bool):
        """Asettelee kortit oikeille paikoille.

        Args:
            cards (list): lista kortteja.
            user (int): 0, jos jakaja, 1 jos pelaaja.
            hand_number (int): pelaajan käden järjestysnumero (1-5).
            message (str): tieto käden arvosta, tai lopputuloksesta.
            active (bool): kertoo, onko tämä käsi, tällä hetkellä, pelivuorossa.
        """
        position_y = 250
        position_x = 160
        if active:
            self.sprites['temp_game_sprites'].add(Button(hand_number * 220 - 35, 220, 'active'))
        for card in cards:
            if user == 0:
                self.sprites['temp_game_sprites'].add(Card(position_x, 20, card.crest()))
            elif user == 1:
                self.sprites['temp_game_sprites'].add(Card(hand_number * 220, position_y, card.crest()))
            position_x += 160
            position_y += 65
        if user == 1:
            self.sprites['temp_game_sprites'].add(Text(message, 20, self._color['white'], hand_number * 220, 220))
        if user == 0:
            self.sprites['temp_game_sprites'].add(Text(message, 30, self._color['white'], 1000, 10))
        if user == 0 and len(cards) == 1:
            self.sprites['temp_game_sprites'].add(CardBack(position_x, 20))


    def hand_compiler(self, player_hands:list, dealer_hand:tuple):
        """Asettelee kaikki kädet, oikealla viestillä, card_compiler funktioon.

        Args:
            player_hands (list): lista pelaajan käsistä.
            dealer_hand (tuple): lista jakajan korteista, ja korttien yhteisarvosta.
        """
        hand_number = 1
        for hand in player_hands:
            if hand.bust():
                self._card_compiler(hand.cards(), 1, hand_number, f'Busted Out!', hand == self._active_hand)
            elif hand.surrender():
                self._card_compiler(hand.cards(), 1, hand_number, f'Surrendered!', hand == self._active_hand)
            elif hand.win():
                self._card_compiler(hand.cards(), 1, hand_number, hand.win_message(), hand == self._active_hand)
            else:
                self._card_compiler(hand.cards(), 1, hand_number, f'Hand value {hand.value()}', hand == self._active_hand)
            hand_number += 1
        self._card_compiler(dealer_hand[0], 0, 0, f'Dealer hand value: {dealer_hand[1]}', False)

    def set_active_hand(self, hand):
        self._active_hand = hand
