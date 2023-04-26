import sqlite3
from build_db import build, drop_tables
from populate_events_table import populate_events
from populate_divisions_table import populate_divisions
from populate_fighter_table import populate_fighters
from populate_referees_table import populate_referees

db_file = 'fight.sqlite'

## hard coding UFC into the database
def insert_ufc(conn, curs):
    query = "INSERT INTO Promotions (promotion) VALUES ('ufc')"
    curs.execute(query)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()

    ## Wipe current db
    drop_tables(curs)

    ## Build the db
    build(curs)
    populate_fighters(conn, curs)
    populate_divisions(conn, curs)
    populate_referees(conn, curs)
    populate_events(conn, curs)
    insert_ufc(conn, curs)

    curs.close()
    conn.close()
