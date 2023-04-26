import csv
import sqlite3
from datetime import datetime
from utils import db_file

def month_to_int(string):
    match string:
        case 'January': return 1
        case 'February': return 2
        case 'March': return 3
        case 'April': return 4
        case 'May': return 5
        case 'June': return 6
        case 'July': return 7
        case 'August': return 8
        case 'September': return 9
        case 'October': return 10
        case 'November': return 11
        case 'December': return 12
        case other: return 0

def parse_date(string):
    month_day = string.split(',')[0]
    day = int(month_day[-2:])
    month = month_to_int(month_day[:-2])
    year = int(string.split(',')[1])
    timestamp = int(datetime(year, month, day).timestamp())
    return timestamp

def populate_events(conn, curs):
    csvpath = '../csv/ufc_fight_outcomes.csv'
    with open(csvpath) as csvfile:
        csvreader = csv.DictReader(csvfile)
        events = []
        for row in csvreader:
            name = row['EventName'].replace("'", "''") ## double ' escapes the quote
            date = str(parse_date(row['EventDate']))
            loc = row['EventLoc'] 

            ### 1 is the id of UFC in the Promotions table
            event = "('{}', {}, '{}', 1)".format(name, date, loc)
            if event not in events: events.append(event)

    events.reverse() ## reverse in place, i want early UFC events with low ids
    query = "INSERT INTO Events ('name', 'date', 'location', 'promotion') VALUES {};".format(', '.join(events))
    curs.execute(query)
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    populate_events(conn, curs)
    curs.close()
    conn.close()
