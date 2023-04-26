import argparse
import csv
import sqlite3
from schema import tables
from utils import add_quotes, format_by_type

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
    'division': 'Division',
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

## Hardcoding this for now
def get_division_id(division):
    match division:
        case 'Flyweight Division':
            return 1
        case 'Bantamweight Division':
            return 2
        case 'Featherweight Division':
            return 3
        case 'Lightweight Division':
            return 4
        case 'Welterweight Division':
            return 5
        case 'Middleweight Division':
            return 6
        case 'Light Heavyweight Division':
            return 7
        case 'Heavyweight Division':
            return 8
        case 'Women\'s Strawweight Division':
            return 9
        case 'Women\'s Flyweight Division':
            return 10
        case 'Women\'s Bantamweight Division':
            return 11
        case 'Women\'s Featherweight Division':
            return 12
        case other:
            return 'NULL'

def populate_fighters(conn, curs):
    with open(csv_path) as csvfile:
        csvreader = csv.DictReader(csvfile)
        values = []
        for row in csvreader:
            row['Division'] = str(get_division_id(row['Division']))
            rowvals = [format_by_type('Fighters', row[translate_cols[key]], key) for key in translate_cols.keys()]
            value = '({})'.format(', '.join(rowvals))
            values.append(value)
    
    cols = ', '.join(map(add_quotes, translate_cols.keys()))
    values = ', '.join(values)
    query = 'INSERT INTO Fighters ({}) VALUES {};'.format(cols, values) 
    curs.execute(query)
    conn.commit()


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
