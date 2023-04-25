import sqlite3
from build_db import build, drop_tables
from populate_fighter_table import populate_fighters

db_file = 'fight.sqlite'

## hard coding UFC into the database
def insert_ufc(conn, curs):
    query = "INSERT INTO Promotions (promotion) VALUES ('ufc')"
    curs.execute(query)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()

    drop_tables(curs)
    build(curs)
    populate_fighters(conn, curs)
    insert_ufc(conn, curs)

    curs.close()
    conn.close()
