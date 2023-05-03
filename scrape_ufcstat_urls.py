import csv
import requests
import string
from bs4 import BeautifulSoup


def get_fighters():
    alphabet = list(string.ascii_lowercase)
    url = 'http://ufcstats.com/statistics/fighters?char={}&page=all'

    fighter_urls = []
    for i in alphabet:
        pageurl = url.format(i)
        response = requests.get(pageurl)
        soup = BeautifulSoup(response.content, 'html.parser')
        fighters = soup.find_all('tr', {'class': 'b-statistics__table-row'})
        for fighter in fighters:
            fighterurl = fighter.find('a', {'class': 'b-link'})
            if not fighterurl:
                continue
            tds = fighter.find_all('td')
            first_name = tds[0].text.strip()
            last_name = tds[1].text.strip()
            name = ' '.join([first_name, last_name])
            UUID = fighterurl['href'].split('/').pop().strip()
            fighter_urls.append([name, UUID])

    return fighter_urls


if __name__ == '__main__':
    fighters = get_fighters()

    with open('csv/ufcstats_uuids.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        for fighter in fighters:
            csvwriter.writerow(fighter)
