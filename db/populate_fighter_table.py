import argparse
import csv
import sqlite3
from schema import tables

csv_path = '../csv/clean_ufc_fighter_data.csv'
db_file = 'fight.sqlite'

## Key - column in Fighter table
## Value - column in csv scraped from UFC site
translate_cols = {
    'name': 'Name',
    'nickname': 'Nickname',
    'wins': 'wins',
    'losses': 'losses',
    'draws': 'draws',
    #'division': 'Division',
    'age': 'Age',
    'height': 'Height',
    'weight': 'Weight',
    'reach': 'Reach',
    'legReach': 'Leg reach',
    'sigStrikesLanded': 'Sig. Strikes Landed',
    'sigStrikesAttempted': 'Sig. Strikes Attempted',
    'sigStrikesHead': 'head total',
    'sigStrikesBody': 'body total',
    'sigStrikesLeg': 'leg total',
    'sigStrikesStanding': 'Standing',
    'sigStrikesClinch': 'Clinch',
    'sigStrikesGround': 'Ground',
    'sigStrikesPerMin': 'Sig. Str. Landed Per Min',
    'sigStrikesAbsorbedPerMin': 'Sig. Str. Absorbed Per Min',
    'takedownsLanded': 'Takedowns Landed',
    'takedownsAttempted': 'Takedowns Attempted',
    'takedownsPer15Min': 'Takedown avg Per 15 Min',
    'submissionAttemptPer15Min': 'Submission avg Per 15 Min',
    'winKO' : 'KO/TKO',
    'winDEC': 'DEC',
    'winSUB': 'SUB',
    'avgFightTime': 'Average fight time',
    'firstRoundFinishes': 'First Round Finishes'
}

def populate_fighters(conn, curs):
    with open(csv_path) as csvfile:
        csvreader = csv.DictReader(csvfile)
        values = []
        for row in csvreader:
            rowvals = [format_by_type(row[translate_cols[key]], key) for key in translate_cols.keys()]
            value = '({})'.format(', '.join(rowvals))
            print(value)
            values.append(value)
    
    cols = ', '.join(map(add_quotes, translate_cols.keys()))
    values = ', '.join(values)
    query = 'INSERT INTO Fighters ({}) VALUES {};'.format(cols, values) 
    curs.execute(query)
    conn.commit()

def add_quotes(string):
    return ''.join(['"', string, '"'])

def format_by_type(string, key):
    key_type = tables['Fighters'][key]
    if not string: 
        return 'NULL'

    match key_type:
        case 'TEXT':
            return add_quotes(string)
        case 'INTEGER':
            if is_number(string):
                return string
            else:
                return 'NULL'
        case 'REAL':
            if is_number(string):
                return string
            else:
                return 'NULL'
        case other:
            return string

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def build_parser():
    parser = argparse.ArgumentParser(description='Populate the Fighters table.')
    parser.add_argument('-D', '--delete', action='store_true', help='Delete all data in Fighters table.')
    return parser

def delete_fighter_data(conn, curs):
    query = "DELETE FROM Fighters;"
    curs.execute(query)
    conn.commit()
        
 
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()

    parser = build_parser()
    args = parser.parse_args()
    if args.delete: delete_fighter_data(conn, curs)

    populate_fighters(conn, curs)

    curs.close()
    conn.close()
