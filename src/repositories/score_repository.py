from db_connection import get_db_connection

class ScoreRepository:
    def __init__(self, db_connection):
        self._db = db_connection

    def get_scores(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT player, score FROM scores ORDER BY score DESC LIMIT 10;")
        return cursor.fetchall()

    def add_score(self, player, score):
        cursor = self._db.cursor()
        cursor.execute("INSERT INTO scores (player, score) VALUES (?, ?);",
        (player, score))
        self._db.commit()

score_repository = ScoreRepository(get_db_connection())
