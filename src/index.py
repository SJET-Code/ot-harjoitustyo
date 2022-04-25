import pygame
from board import Board
from gameloop import GameLoop
from event_queue import EventQueue
from renderer import Renderer
from clock import Clock


def main():

    display_height = 720
    display_width = 1360
    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Blackjack")

    board = Board()
    event_queue = EventQueue()
    renderer = Renderer(display, board)
    clock = Clock()
    game_loop = GameLoop(board, renderer, event_queue, clock)

    pygame.init()
    display.fill((46, 125, 50, 1))
    pygame.display.update()
    game_loop.start()


if __name__ == "__main__":
    main()
