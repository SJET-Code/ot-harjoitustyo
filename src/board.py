import pygame
from sprites.card import Card
from sprites.card_back import CardBack
from sprites.deck import DeckSprite
from sprites.text import Text


class Board:
    def __init__(self, display):
        self.cards = pygame.sprite.Group()
        self.deck = DeckSprite(0, 0)
        self.start_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()
        self.temp_game_sprites = pygame.sprite.Group()
        self.start = True
        self.game = False
        self.display = display
        self.start_sprites.add(
            Text('New Game (n)', 30, (255, 255, 255), 1360//2-60, 720//2-60))

    def game_update(self, player_credits, player_cards, dealer_cards, game_state):
        self.temp_game_sprites.empty()
        if game_state == 0:
            self.card_compiler(dealer_cards[0],0,0)
            self.card_compiler(player_cards[0],1,0)
            self.temp_game_sprites.add(
                Text(f'HAND VALUE: {player_cards[1]}', 30, (255, 255, 255), 500, 550))
            self.temp_game_sprites.add(
                Text(f'DEALER HAND VALUE: {dealer_cards[1]}', 30, (255, 255, 255), 800, 550))
            self.temp_game_sprites.add(
                Text('HIT (spacebar)', 50, (255, 255, 255), 600, 650))
            self.temp_game_sprites.add(
                Text('STAY (s)', 50, (255, 255, 255), 300, 650))
            self.temp_game_sprites.add(
                Text(f'CREDITS: {player_credits}', 30, (255, 255, 255), 10, 650))
        elif game_state == 1:
            self.card_compiler(dealer_cards[0],0,1)
            self.card_compiler(player_cards[0],1,1)
            self.temp_game_sprites.add(
                Text(f'HAND VALUE: {player_cards[1]}', 30, (255, 255, 255), 500, 550))
            self.temp_game_sprites.add(
                Text(f'DEALER HAND VALUE: {dealer_cards[1]}', 30, (255, 255, 255), 800, 550))
            self.temp_game_sprites.add(
                Text(f'CREDITS: {player_credits}', 30, (255, 255, 255), 10, 650))
            self.temp_game_sprites.add(
                Text('NEXT CARD (spacebar)', 50, (255, 255, 255), 600, 650))

    def place_bet(self, bet: int, player_credits: int):
        self.temp_game_sprites.empty()
        self.temp_game_sprites.add(
            Text(f'BET: {bet}, (arrow keys + spacebar)', 30, (255, 255, 255), 10, 550))
        self.temp_game_sprites.add(
            Text(f'CREDITS: {player_credits-bet}', 30, (255, 255, 255), 10, 650))

    def round_end(self, player_credits: int, win: bool):
        if win:
            self.temp_game_sprites.add(
                Text('You won! Press \'spacebar\' for a new round and \'r\' to retire',
                     30, (255, 255, 255), 300, 300))
        elif player_credits >= 5:
            self.temp_game_sprites.add(
                Text('You lost! Press \'spacebar\' for a new round and \'r\' to retire',
                     30, (255, 255, 255), 300, 300))
        else:
            self.temp_game_sprites.add(
                Text('You lost! Press \'n\' to start a new game',
                     30, (255, 255, 255), 300, 300))

    def bust_out(self, player_credits: int):
        if player_credits >= 5:
            self.temp_game_sprites.add(
                Text('You busted out! Press \'spacebar\' for a new round and \'r\' to retire',
                     30, (255, 255, 255), 300, 300))
        else:
            self.temp_game_sprites.add(
                Text('You busted out!! Press \'n\' to start a new game',
                     30, (255, 255, 255), 300, 300))

    def start_game(self):
        self.start = False
        self.game = True
        self.game_sprites.add(self.deck)

    def card_compiler(self, cards:list, user:int, state:int):
        position=100
        for card in cards:
            if user==0:
                self.temp_game_sprites.add(Card(position, 20, card.crest()))
            elif user==1:
                self.temp_game_sprites.add(Card(position, 350, card.crest()))
            position+=180
        if user==0==state:
            self.temp_game_sprites.add(CardBack(position, 20))
