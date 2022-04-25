import unittest
from gameloop import GameLoop
from board import Board

class StubClock:
    def tick(self, fps):
        pass
    
    def get_ticks(self):
        return 0




class TestGameLoop(unittest.TestCase):
    def setUp(self):
        self.board = GameLoop(Board(),)