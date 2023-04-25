import sqlite3
from utils import db_file

divisions = [('Flyweight', 125, 'M'),
             ('Bantamweight', 135, 'M'),
             ('Featherweight', 145, 'M'),
             ('Lightweight', 155, 'M'),
             ('Welterweight', 170, 'M'),
             ('Middleweight', 185, 'M'),
             ('Light Heavyweight', 205, 'M'),
             ('Heavyweight', 265, 'M'),
             ('Strawweight', 115, 'F'),
             ('Flyweight', 125, 'F'),
             ('Bantamweight', 135, 'F'),
             ('Featherweight', 145, 'F')]

def populate_divisions(conn, curs):
    values = []
    for division in divisions:
        value = '(\'{}\', {}, \'{}\')'.format(division[0], division[1], division[2])
        values.append(value)

    query = 'INSERT INTO Divisions (division, weight, gender) VALUES {};'.format(', '.join(values))
    curs.execute(query)
    conn.commit()
    
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    populate_divisions(conn, curs)
    curs.close()
    conn.close()
