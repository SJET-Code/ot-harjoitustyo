import unittest
from repositories.score_repository import ScoreRepository
from db_connection import get_db_connection
from init_database import init_database

class TestScoreRepository(unittest.TestCase):
    def setUp(self):
        init_database()
        self.scores = ScoreRepository(get_db_connection())

    def test_get_scores_returns_empty_list_when_db_is_empty(self):
        self.assertEqual(self.scores.get_scores(), [])

    def test_add_score_adds_correct_information_in_database(self):
        self.scores.add_score('SJE', 500)
        self.assertEqual((self.scores.get_scores()[0]['player'], self.scores.get_scores()[0]['score']), ('SJE', 500))
