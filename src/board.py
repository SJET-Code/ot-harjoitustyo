import pygame
from sprites.card import Card
from sprites.card_back import Card_Back
from sprites.deck import Deck_Sprite
from sprites.text import Text


class Board:
    def __init__(self,display):
        self.cards = pygame.sprite.Group()
        self.card_backs = pygame.sprite.Group()
        self.deck = Deck_Sprite(0,0)
        self.start_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()
        self.temp_game_sprites = pygame.sprite.Group()
        self.start = True
        self.game = False
        self.display=display
        self.start_sprites.add(Text('New Game (n)',30,(255,255,255),1360//2-60,720//2-60))

    def game_update(self, credits:int, player_cards:tuple, dealer_cards:tuple, game_state:int):
        self.temp_game_sprites.empty()
        if game_state==0:
            dealer_pos=100
            for card in dealer_cards[0]:
                self.temp_game_sprites.add(Card(dealer_pos,20,card.crest()))
                dealer_pos+=180
            self.temp_game_sprites.add(Card_Back(dealer_pos,20))
            player_pos=100
            for card in player_cards[0]:
                self.temp_game_sprites.add(Card(player_pos,350,card.crest()))
                player_pos+=180
            self.temp_game_sprites.add(Text(f'HAND VALUE: {player_cards[1]}',30,(255,255,255),500,550))
            self.temp_game_sprites.add(Text(f'DEALER HAND VALUE: {dealer_cards[1]}',30,(255,255,255),800,550))
            self.temp_game_sprites.add(Text('HIT (spacebar)',50,(255,255,255),600,650))
            self.temp_game_sprites.add(Text('STAY (s)',50,(255,255,255),300,650))
            self.temp_game_sprites.add(Text(f'CREDITS: {credits}',30,(255,255,255),10,650))
        elif game_state==1:
            dealer_pos=100
            for card in dealer_cards[0]:
                self.temp_game_sprites.add(Card(dealer_pos,20,card.crest()))
                dealer_pos+=180
            player_pos=100
            for card in player_cards[0]:
                self.temp_game_sprites.add(Card(player_pos,350,card.crest()))
                player_pos+=180
            self.temp_game_sprites.add(Text(f'HAND VALUE: {player_cards[1]}',30,(255,255,255),500,550))
            self.temp_game_sprites.add(Text(f'DEALER HAND VALUE: {dealer_cards[1]}',30,(255,255,255),800,550))
            self.temp_game_sprites.add(Text(f'CREDITS: {credits}',30,(255,255,255),10,650))
            self.temp_game_sprites.add(Text('NEXT CARD (spacebar)',50,(255,255,255),600,650))


    def place_bet(self, bet:int, credits:int):
        self.temp_game_sprites.empty()
        self.temp_game_sprites.add(Text(f'BET: {bet}, use arrows up and down to increase/decrease the bet and spacebar to confirm',30,(255,255,255),10,550))
        self.temp_game_sprites.add(Text(f'CREDITS: {credits-bet}',30,(255,255,255),10,650))

    def round_end(self, credits:int, win:bool):
        if win:
            self.temp_game_sprites.add(Text('You won! Press \'spacebar\' for a new round and \'r\' to retire',30,(255,255,255),300,300))
        elif credits>=5:
            self.temp_game_sprites.add(Text('You lost! Press \'spacebar\' for a new round and \'r\' to retire',30,(255,255,255),300,300))
        else:
            self.temp_game_sprites.add(Text('You lost! Press \'n\' to start a new game',30,(255,255,255),300,300))

    def bust_out(self, credits:int):
        if credits>=5:
            self.temp_game_sprites.add(Text('You busted out! Press \'spacebar\' for a new round and \'r\' to retire',30,(255,255,255),300,300))
        else:
            self.temp_game_sprites.add(Text('You busted out!! Press \'n\' to start a new game',30,(255,255,255),300,300))

    def start_game(self):
        self.start=False
        self.game=True
        self.game_sprites.add(self.deck)

            
