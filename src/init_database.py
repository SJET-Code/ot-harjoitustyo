from db_connection import get_db_connection

def reset_tables(database):
    cursor = database.cursor()
    cursor.execute("DROP TABLE IF EXISTS scores;")
    cursor.execute("""
        CREATE TABLE scores (
            id INTEGER PRIMARY KEY,
            player VARCHAR(3),
            score INTEGER
        );
    """)
    database.commit()


def init_database():
    database = get_db_connection()
    reset_tables(database)


if __name__ == "__main__":
    init_database()
