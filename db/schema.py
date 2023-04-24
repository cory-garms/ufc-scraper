import argparse
import sqlite3

db_file = "fight.sqlite"
tables = {
    'Events': {
        'id': 'INTEGER PRIMARY KEY ASC',
    },

    'Fighters': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'name': 'TEXT',
        'nickname': 'TEXT'
    },

    'FighterStatHistory': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'fighter': 'INTEGER',
        'event': 'INTEGER'
    },

    'Fights': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'event': 'INTEGER',
        'fighter1': 'INTEGER',
        'fighter2': 'INTEGER' 
    },

    'FightStats': {
        'id': 'INTEGER PRIMARY KEY ASC',
        'fight': 'INTEGER',
        'fighter': 'INTEGER'
    }
}

foreign_keys = {
    'FighterStatHistory': [('fighter', 'Fighters(id)'),
                           ('event', 'Events(id)')],

    'Fights': [('event', 'Events(id)'),
               ('fighter1', 'Fighters(id)'),
               ('fighter2', 'Fighters(id)')],

    'FightStats': [('fight', 'Fights(id)'),
                   ('fighter', 'Fighters(id)')]
}


def build():
   for table in tables.keys():
        create = "CREATE TABLE IF NOT EXISTS {}".format(table)
        cols = []
        fkeys = []

        for key, value in tables[table].items():
            col = "{} {}".format(key, value)
            cols.append(col) 

        if table in foreign_keys.keys():
            for fkey in foreign_keys[table]:
                fkeys.append('FOREIGN KEY({}) REFERENCES {}'.format(fkey[0], fkey[1]))
                
        col_str = ','.join(cols)
        fkey_str = ','.join(fkeys)
        strings = [col_str, fkey_str]
        strings = [x for x in strings if x] ## filter out empty strings

        query = create + " ({})".format(','.join(strings))
        print(query)
        curs.execute(query) 
        
def drop_tables():
    for table in tables.keys():
        query = "DROP TABLE IF EXISTS {}".format(table)
        curs.execute(query)

def build_parser():
    parser = argparse.ArgumentParser(description='Build the fight database.')
    parser.add_argument('-b', '--build', action='store_true', help='create the schema for fight.sqlite')
    parser.add_argument('-D', '--drop', action='store_true', help='Drop all tables in fight.sqlite')
    return parser

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()

    if args.build: build()
    if args.drop: drop_tables()

    curs.close()
    conn.close()
