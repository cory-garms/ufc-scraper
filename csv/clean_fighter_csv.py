import csv
import re

csv_path = 'ufc_fighter_data.csv'
clean_csv_path = 'clean_ufc_fighter_data.csv'

def clean_percents(string):
    return string.split(' ')[0]

def time_to_seconds(time):
    if time: 
        mins = int(time.split(':')[0])
        secs = int(time.split(':')[1])
        return (mins*60) + secs
    else:
        return 0

def parse_record(record):
    pattern = re.compile('(W-L-D)')
    if pattern.search(record):
        record = record.split(' ')[0]
        wins = int(record.split('-')[0])
        losses = int(record.split('-')[1])
        draws = int(record.split('-')[2])
        return wins, losses, draws
    else:
        return 0, 0, 0

if __name__ == '__main__':
    with open(csv_path) as infile, open(clean_csv_path, 'w') as outfile:
        csvreader = csv.DictReader(infile)
        colnames = csvreader.fieldnames + ['wins', 'losses', 'draws']
        csvwriter = csv.DictWriter(outfile, colnames)
        csvwriter.writeheader()
        for row in csvreader:
            row['Standing'] = clean_percents(row['Standing'])
            row['Clinch'] = clean_percents(row['Clinch'])
            row['Ground'] = clean_percents(row['Ground'])
            row['KO/TKO'] = clean_percents(row['KO/TKO'])
            row['DEC'] = clean_percents(row['DEC'])
            row['SUB'] = clean_percents(row['SUB'])
            row['Average fight time'] = time_to_seconds(row['Average fight time'])
            row['wins'], row['losses'], row['draws'] = parse_record(row['Record'])

            csvwriter.writerow(row)
