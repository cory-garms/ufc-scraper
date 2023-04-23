import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

####ODDS API KEY
api_key = os.getenv("api_key")  # in bash, use 'set -a; source .env; set +a' to connect .env file containing api key


#function to get list of all events from UFC site and convert them to urls that display search results for each event
def get_search_results():
    eventnames=[]

    # URL of the website that contains the event links
    url = 'http://ufcstats.com/statistics/events/completed?page=all'

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div that contains the event links
    event_div = soup.find('tbody')

    # Extract the event names and convert them to search query urls
    event_urls = []
    for event_link in event_div.find_all('a'):
        eventnames.append('https://www.bestfightodds.com/search?query=' + event_link.text.strip().replace(':','+60%3A').replace(' ', '+'))

    return eventnames

#function to scape data from ' https://www.bestfightodds.com/archive' by searching for strings of known events
def search_scraper(url):

    fighturls = []

    # Send a GET request to the website
    response = requests.get(url)

    print('Searching: ' + url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # Find the div that contains the event links
        event_div = soup.find_all('table', {'class':'content-list'})[1]

        for event in event_div.find_all('a'):
            if 'ufc' in event['href']:
                tryurl = 'https://www.bestfightodds.com' + event['href']
                fighturls.append(tryurl)

        return fighturls

    except:
        print('Search returned no events.')

#run this to populate list of search result urls
# events = get_search_results()

#function that uses the search_scraper function and list of eventurls to harvest the urls of all completed ufc events and write them to a csv file
def harvest_urls():
    uniqueevents= []
    for url in events:
        print(url)
        tryurls = search_scraper(url)
        if tryurls:
            for t in tryurls:
                if t not in uniqueevents:
                    uniqueevents.append(t)
        print('list length: ' + str(len(uniqueevents)))

    pd.DataFrame(uniqueevents, columns=["event_url"]).to_csv('fight_odds_urls.csv')
    return uniqueevents


def scrape_odds(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    event = soup.find('h1').text
    date = soup.find('span', {'class':'table-header-date'}).text

    # Find the div that contains the event links
    table_div = soup.find('div', {'class':'table-div'})

    df = pd.read_html(str(table_div))[1]

    df.rename( columns={'Unnamed: 0':'Name'}, inplace=True )

    df[df['Name'].apply(lambda x: True if len(str(x).split()) == 2 else False)]


    oddsDF = pd.DataFrame(columns=['Event', 'Date', 'Name', 'Opponent', '5D_odds' ])

    oddsDF['5D_odds'] = df[['5D']]
    oddsDF['Name'] = df[['Name']]
    oddsDF['Date'] = date
    oddsDF['Event'] = event

    for i in range(len(oddsDF)):
        #print(oddsDF.iloc[i]['Opponent'])
        if i % 2:
            oddsDF.at[i, 'Opponent'] = oddsDF.iloc[i-1]['Name']
        else:
            oddsDF.at[i, 'Opponent'] = oddsDF.iloc[i+1]['Name']

    return oddsDF
            

df = pd.read_csv('fight_odds_urls.csv', delimiter=',')

sample_url = df['event_url'][1]

agg_odds_df = pd.DataFrame()

for url in df['event_url'][0:4]:
    try:
        odds = scrape_odds(url)

        agg_odds_df = pd.concat([agg_odds_df, odds])
    except: 
        print('Failed to capture table')


print(agg_odds_df.reset_index().tail())

agg_odds_df.to_csv('aggregate_odds.csv')

#####~~~  ODDS API SECTION    ~~~####
# # First get a list of in-season sports
# sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
#     'api_key': api_key
# })

# sports_json = json.loads(sports_response.text)

# if not sports_json['success']:
#     print(
#         'There was a problem with the sports request:',
#         sports_json['msg']
#     )

# else:
#     print()
#     print(
#         'Successfully got {} sports'.format(len(sports_json['data'])),
#         'Here\'s the first sport:'
#     )
#     print(sports_json['data'][0])



# # To get odds for a sepcific sport, use the sport key from the last request
# #   or set sport to "upcoming" to see live and upcoming across all sports
# sport_key = 'mma_mixed_martial_arts'

# odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
#     'api_key': api_key,
#     'sport': sport_key,
#     'site_key': 'draftkings',
#     'region': 'us' # uk | us | eu | au
#     #'mkt': 'totals' # h2h | spreads | totals
# })

# odds_json = json.loads(odds_response.text)
# if not odds_json['success']:
#     print(
#         'There was a problem with the odds request:',
#         odds_json['msg']
#     )

# else:
#     # odds_json['data'] contains a list of live and 
#     #   upcoming events and odds for different bookmakers.
#     # Events are ordered by start time (live events are first)
#     print()
#     print(
#         'Successfully got {} events'.format(len(odds_json['data'])),
#         'Here\'s the first event:'
#     )
#     print(odds_json['data'])

#     # Check your usage
#     print()
#     print('Remaining requests', odds_response.headers['x-requests-remaining'])
#     print('Used requests', odds_response.headers['x-requests-used'])