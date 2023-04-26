import csv
import sqlite3
from utils import add_quotes, db_file

def populate_referees(conn, curs):
    csvpath = '../csv/ufc_fight_outcomes.csv'
    with open(csvpath) as csvfile:
        csvreader = csv.DictReader(csvfile)

        ## get unique refs
        referees = list(set([''.join(['(','\'',row['Referee'],'\'',')']) for row in csvreader]))
        
        query = "INSERT INTO Referees (name) VALUES {};".format(', '.join(referees))
        curs.execute(query)
        conn.commit() 

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()

    populate_referees(conn, curs)

    curs.close()
    conn.close()
