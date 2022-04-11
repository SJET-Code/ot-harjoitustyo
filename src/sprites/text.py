import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, x, y):
        super().__init__()
        pygame.init()
        self.font = pygame.font.SysFont('impact', size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y