import pygame


class EventQueue:
    """Hakee pelaajan näppäintapahtumia.
    """
    def get(self):
        """Kutsuu tapahtuman kertovaa funktiota.

        Returns:
            pygame.event: pelaajan näppäintapahtuma.
        """
        return pygame.event.get()
