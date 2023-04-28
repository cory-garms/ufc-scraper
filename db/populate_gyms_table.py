import csv
import sqlite3
from utils import db_file, escape_quotes

def populate_gyms(conn, curs):
    csvpath = '../csv/ufc_fighter_data.csv'
    with open(csvpath) as csvfile:
        csvreader = csv.DictReader(csvfile)

        ## get unique gyms 
        gyms = list(set([''.join(['(','\'',escape_quotes(row['Trains at']),'\'',')']) for row in csvreader]))
        
        query = "INSERT INTO Gyms ('name') VALUES {};".format(', '.join(gyms))
        curs.execute(query)
        conn.commit() 

if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    curs = conn.cursor()
    populate_gyms(conn, curs)
    curs.close()
    conn.close()
