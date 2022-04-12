import os
import pygame


dirname = os.path.dirname(__file__)


def load_sprite(sprite: str):
    return pygame.image.load(os.path.join(dirname, "assets", sprite+'.png'))
