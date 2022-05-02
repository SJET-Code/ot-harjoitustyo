import pygame
from ui.image_loader import load_sprite


class CardBack(pygame.sprite.Sprite):
    def __init__(self, x_position=0, y_position=0):
        super().__init__()
        self.image = load_sprite('CardBack')
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def height(self):
        return self.image.get_height()

    def width(self):
        return self.image.get_width()
