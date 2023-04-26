import argparse
import sqlite3
from schema import tables, foreign_keys

db_file = "fight.sqlite"

def build(curs):
   for table in tables.keys():
        create = "CREATE TABLE IF NOT EXISTS {}".format(table)
        cols = []
        fkeys = []

        for key, value in tables[table].items():
            if 'constraint' in value.keys():
                col = "{} {} {}".format(key, value['type'], value['constraint'])
            else:
                col = "{} {}".format(key, value['type'])
            cols.append(col) 

        if table in foreign_keys.keys():
            for fkey in foreign_keys[table]:
                fkeys.append('FOREIGN KEY({}) REFERENCES {}'.format(fkey[0], fkey[1]))
                
        col_str = ','.join(cols)
        fkey_str = ','.join(fkeys)
        strings = [col_str, fkey_str]
        strings = [x for x in strings if x] ## filter out empty strings

        query = create + " ({})".format(','.join(strings))
        curs.execute(query) 
        
def drop_tables(curs):
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

    if args.build: build(curs)
    if args.drop: drop_tables(curs)

    curs.close()
    conn.close()
