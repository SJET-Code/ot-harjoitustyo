import os
import pygame


dirname = os.path.dirname(__file__)


def load_sprite(sprite: str):
    """Hakee assets kansiosta halutun kuvan, mikä piirretään ruudulle.

    Args:
        sprite (str): kuvan nimi.

    Returns:
        pygame.image: piirrettävä kuva.
    """
    return pygame.image.load(os.path.join(dirname, "assets", sprite+'.png'))
