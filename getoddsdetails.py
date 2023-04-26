import pandas as pd
from bs4 import BeautifulSoup
import requests



#function to get list of all events from UFC site and convert them to urls that display search results for each event
def get_name_search_urls():
    df = pd.read_csv('./csv/clean_ufc_fighter_data.csv')

    names = df['Name']

    # Extract the event names and convert them to search query urls
    name_urls = []
    for name in names:
        name_urls.append('https://www.bestfightodds.com/search?query=' + name.replace(':','+60%3A').replace(' ', '+'))

    return name_urls

searchurls = get_name_search_urls()

#function to scape data from ' https://www.bestfightodds.com/archive' by searching for strings of known events
def search_scraper(url):


    nameurls = []

    # Send a GET request to the website
    response = requests.get(url)

    print('Searching: ' + url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    
    try:
        # Find the div that contains the event links
        fighters_div = soup.find_all('table', {'class':'content-list'})[0]

        for fighter in fighters_div.find_all('a'):            
            tryurl = 'https://www.bestfightodds.com' + fighter['href']
            nameurls.append(tryurl)

    except:
        print('Search returned no events.')

    return nameurls


def harvest_urls(nameurls):
    uniquenames= []
    for url in nameurls:
        print(url)
        tryurls = search_scraper(url)
        if tryurls:
            for t in tryurls:
                if t not in uniquenames:
                    uniquenames.append(t)
        print('list length: ' + str(len(uniquenames)))

    pd.DataFrame(uniquenames, columns=["event_url"]).to_csv('./odds/fighter_odds_urls.csv')
    return uniquenames

#harvest_urls(searchurls)

def scrape_odds_details(fighterurl):

    # Send a GET request to the website
    response = requests.get(fighterurl)

    print('Searching: ' + fighterurl)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table')[0]
    
    df = pd.read_html(str(table))[0]

    df.rename( columns={'Unnamed: 6':'mvmt'}, inplace=True )

    events, fighters, opponents, opening_odds, closing_odds1, closing_odds2, movement = ([] for i in range(7)) 

    for index, row in df.iterrows():
        if 'UFC' in str(row['Event']):
            if 'UFC' in str(row['Matchup']):
                events.append(str(row['Event']))
                fighters.append(df.iloc[index+1]['Matchup'])
                opponents.append(df.iloc[index+2]['Matchup'])
                opening_odds.append(df.iloc[index+1]['Open'])
                closing_odds1.append(df.iloc[index+1]['Closing range'])
                closing_odds2.append(df.iloc[index+1]['Closing range.2'])
                movement.append(df.iloc[index+1]['mvmt'])

    oddsdf = pd.DataFrame({'Event': events, 'Fighter':fighters, 'Opponent': opponents, 'Opening_odds': opening_odds,'Close_odds1': closing_odds1,'Close_odds2': closing_odds2,'Movement': movement})
    
    return oddsdf

detailed_odds = pd.DataFrame

df = pd.read_csv('./odds/fighter_odds_urls.csv', delimiter=',')

sample_url = df['event_url'][1]

agg_odds_df = pd.DataFrame()

for index, url in enumerate(df['event_url']):

    if index % 250 == 0:
        agg_odds_df.to_csv('./odds/odds_movement.csv', index=False)
        print(f'###########      finished scraping up to index {str(index)}    ######')

    try:
        new_odds = scrape_odds_details(url)
        agg_odds_df = pd.concat([agg_odds_df, new_odds])

    except: 
        print(f'could not scrape odds data from {url}')

print(agg_odds_df)

agg_odds_df.to_csv('./odds/odds_movement0.csv', index=False)