import unittest
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_start_game_makes_state_game_true(self):
        self.board.start_game()
        self.assertTrue(self.board.state['game'])

    def test_start_game_makes_state_start_false(self):
        self.board.start_game()
        self.assertFalse(self.board.state['start'])
    
    def test_start_game_makes_state_adds_a_sprite_to_game_sprites(self):
        self.board.start_game()
        self.assertTrue(len(self.board.sprites['game_sprites']) == 1)

    def test_place_bet_clears_temp_game_sprites_and_adds_5_sprites(self):
        self.board.place_bet(5, 100)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == 5)
    
    def test_round_end_adds_5_sprites_when_win(self):
        test = len(self.board.sprites['temp_game_sprites'])
        self.board.round_end(100, True)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == test+5)

    def test_round_end_adds_5_sprites_when_lose_and_have_atleast_5_credits(self):
        test = len(self.board.sprites['temp_game_sprites'])
        self.board.round_end(5, False)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == test+5)

    def test_round_end_adds_3_sprites_when_lose_and_have_less_than_5_credits(self):
        test = len(self.board.sprites['temp_game_sprites'])
        self.board.round_end(4, False)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == test+3)

    def test_bust_out_adds_3_sprites_when_have_less_than_5_credits(self):
        test = len(self.board.sprites['temp_game_sprites'])
        self.board.bust_out(4)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == test+3)

    def test_bust_out_adds_5_sprites_when_have_atleast_5_credits(self):
        test = len(self.board.sprites['temp_game_sprites'])
        self.board.bust_out(5)
        self.assertTrue(len(self.board.sprites['temp_game_sprites']) == test+5)