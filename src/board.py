import pygame
from sprites.card import Card
from sprites.card_back import CardBack
from sprites.deck import DeckSprite
from sprites.text import Text
from sprites.button import Button
from repositories.score_repository import score_repository

class Board:
    def __init__(self):
        self.sprites = {
            'start_sprites' : pygame.sprite.Group(),
            'game_sprites' : pygame.sprite.Group(),
            'temp_game_sprites' : pygame.sprite.Group(),
            'end_sprites' : pygame.sprite.Group(),
            'temp_end_sprites' : pygame.sprite.Group()
        }
        self.player_name = ""
        self.score = 0
        self.state = {'start' : True, 'game' : False, 'end' : False}
        text = Text('New Game', 80, (255, 255, 255), 1330//2-200, 600)
        self.sprites['start_sprites'].add(
            text,
            Button(1330//2-200+text.width()+10, 630, 'n')
            )

    def game_update(self, player_credits, player_cards, dealer_cards, game_state):
        self.sprites['temp_game_sprites'].empty()
        if game_state == 0:
            self.card_compiler(dealer_cards[0],0,0)
            self.card_compiler(player_cards[0],1,0)
            hit = Text('HIT', 50, (255, 255, 255), 600, 650)
            stay = Text('STAY', 50, (255, 255, 255), 300, 650)
            self.sprites['temp_game_sprites'].add(
                Text(f'HAND VALUE: {player_cards[1]}', 30, (255, 255, 255), 500, 550),
                Text(f'DEALER HAND VALUE: {dealer_cards[1]}', 30, (255, 255, 255), 800, 550),
                hit,
                Button(600+hit.width()+10, 660, 'space'),
                stay,
                Button(300+stay.width()+10, 660, 's'),
                Text(f'CREDITS: {player_credits}', 30, (255, 255, 255), 10, 650)
            )
        elif game_state == 1:
            self.card_compiler(dealer_cards[0],0,1)
            self.card_compiler(player_cards[0],1,1)
            text = Text('NEXT CARD', 50, (255, 255, 255), 600, 650)
            self.sprites['temp_game_sprites'].add(
                Text(f'HAND VALUE: {player_cards[1]}', 30, (255, 255, 255), 500, 550),
                Text(f'DEALER HAND VALUE: {dealer_cards[1]}', 30, (255, 255, 255), 800, 550),
                Text(f'CREDITS: {player_credits}', 30, (255, 255, 255), 10, 650),
                text,
                Button(600+text.width()+10, 660, 'space')
                )

    def place_bet(self, bet: int, player_credits: int):
        self.sprites['temp_game_sprites'].empty()
        text = Text(f'BET: {bet}', 30, (255, 255, 255), 10, 550)
        button = Button(10, 440, 'return')
        self.sprites['temp_game_sprites'].add(
            text,
            Text(f'CREDITS: {player_credits-bet}', 30, (255, 255, 255), 10, 650),
            Button(text.width()+20, 530, 'arrows'),
            button,
            Text('TO CONFIRM BET', 30, (255, 255, 255), button.width()+20, 470)
            )

    def round_end(self, player_credits: int, win: bool):
        if win:
            text1 = Text('You won! Press',
                     30, (255, 255, 255), 300, 300)
            button1 = Button(310 + text1.width(), 300, 'space')
            text2 = Text('for a new round and',
                     30, (255, 255, 255), 320 + button1.width() + text1.width(), 300)
            button2 = Button(330 + button1.width() + text2.width() + text1.width(), 300, 'r')
            text3 = Text('to retire',
                     30, (255, 255, 255), 340 + button1.width() + text2.width() +
                     button2.width() + text1.width(), 300)
            self.sprites['temp_game_sprites'].add(
                text1, text2, text3,
                button1, button2
                )
        elif player_credits >= 5:
            text1 = Text('You lost! Press',
                     30, (255, 255, 255), 300, 300)
            button1 = Button(310 + text1.width(), 300, 'space')
            text2 = Text('for a new round and',
                     30, (255, 255, 255), 320 + button1.width() + text1.width(), 300)
            button2 = Button(330 + button1.width() + text2.width() + text1.width(), 300, 'r')
            text3 = Text('to retire',
                     30, (255, 255, 255), 340 + button1.width() + text2.width() +
                     button2.width() + text1.width(), 300)
            self.sprites['temp_game_sprites'].add(
                text1, text2, text3,
                button1, button2
                )
        else:
            text1 = Text('You lost! Press',
                     30, (255, 255, 255), 300, 300)
            button1 = Button(310 + text1.width(), 300, 'n')
            text2 = Text('to start a new game',
                     30, (255, 255, 255), 320 + button1.width() + text1.width(), 300)
            self.sprites['temp_game_sprites'].add(
                text1, text2, button1)

    def bust_out(self, player_credits: int):
        if player_credits >= 5:
            text1 = Text('You busted out! Press',
                     30, (255, 255, 255), 300, 300)
            button1 = Button(310 + text1.width(), 300, 'space')
            text2 = Text('for a new round and',
                     30, (255, 255, 255), 320 + button1.width() + text1.width(), 300)
            button2 = Button(330 + button1.width() + text2.width() + text1.width(), 300, 'r')
            text3 = Text('to retire',
                     30, (255, 255, 255), 340 + button1.width() + text2.width() +
                     button2.width() + text1.width(), 300)
            self.sprites['temp_game_sprites'].add(
                text1, text2, text3,
                button1, button2
                )
        else:
            text1 = Text('You busted out! Press',
                     30, (255, 255, 255), 300, 300)
            button1 = Button(310 + text1.width(), 300, 'n')
            text2 = Text('to start a new game',
                     30, (255, 255, 255), 320 + button1.width() + text1.width(), 300)
            self.sprites['temp_game_sprites'].add(
                text1, text2, button1)

    def start_game(self):
        self.state['start'] = False
        self.state['game'] = True
        self.sprites['game_sprites'].add(DeckSprite(0, 0))

    def end_game(self, score):
        self.state['game'] = False
        self.state['end'] = True
        self.score = score
        self.load_scoreboard()
        self.sprites['temp_end_sprites'].add(Text(f'Your score is {self.score} add a name:',
        30, (255, 255, 255), 350, 600)
        )

    def user_input(self, name:str):
        self.player_name = name.upper()
        self.sprites['temp_end_sprites'].empty()
        text = Text(self.player_name, 50, (255, 255, 255), 720, 590)
        button = Button(720+text.width()+10, 570, 'return')
        self.sprites['temp_end_sprites'].add(
            text,
            button,
            Text(f'Your score is {self.score} add a name:', 30, (255, 255, 255), 350, 600),
            Text('to confirm', 30, (255, 255, 255), 720+text.width()+20+button.width(),600)
        )

    def load_scoreboard(self):
        self.sprites['end_sprites'].empty()
        scores = score_repository.get_scores()
        self.sprites['end_sprites'].add(
            Text('Highscores:', 50, (255, 255, 255), 530, 10))
        y_position = 100
        place = 1
        for row in scores:
            self.sprites['end_sprites'].add(
                Text(f"{place}. {row['player']}", 30, (255, 255, 255), 455, y_position),
                Text(f"SCORE: {row['score']}", 30, (255, 255, 255), 755, y_position)
            )
            place += 1
            y_position += 40

    def confirm_user_input(self):
        score_repository.add_score(self.player_name, self.score)
        self.sprites['temp_end_sprites'].empty()
        self.load_scoreboard()
        self.state['end'] = False
        self.state['start'] = True
        self.player_name = ""

    def card_compiler(self, cards:list, user:int, state:int):
        position=150
        for card in cards:
            if user==0:
                self.sprites['temp_game_sprites'].add(Card(position, 20, card.crest()))
            elif user==1:
                self.sprites['temp_game_sprites'].add(Card(position, 350, card.crest()))
            position+=180
        if user==0==state:
            self.sprites['temp_game_sprites'].add(CardBack(position, 20))
