import os
import sqlite3
from config import DATABASE_FILENAME

dirname = os.path.dirname(__file__)

db = sqlite3.connect(os.path.join(dirname, "..", "data", DATABASE_FILENAME))
db.row_factory = sqlite3.Row


def get_db_connection():
    return db
