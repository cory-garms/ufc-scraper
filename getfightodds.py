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

##run this to populate list of search result urls
# events = get_search_results()

#function that uses the search_scraper function and list of eventurls to harvest the urls of all completed ufc events and write them to a csv file
def harvest_urls(eventurls):
    uniqueevents= []
    for url in eventurls:
        print(url)
        tryurls = search_scraper(url)
        if tryurls:
            for t in tryurls:
                if t not in uniqueevents:
                    uniqueevents.append(t)
        print('list length: ' + str(len(uniqueevents)))

    pd.DataFrame(uniqueevents, columns=["event_url"]).to_csv('./odds/fight_odds_urls.csv')
    return uniqueevents

##run this to scrape urls from bestfightodds
#harvest_urls(events)

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

    df = df.replace('Germaine de Randamie', 'Germaine DeRandamie')
    df = df.replace('Seung Woo Choi', 'Seung WooChoi')
    df = df.replace('Daniel da Silva', 'Daniel DaSilva')
    df = df.replace('Zarah Fairn Dos Santos', 'ZarahFairn DosSantos')
    df = df.replace('Kai Kara France', 'Kai KaraFrance')
    df = df.replace('Alex da Silva', 'Alex DaSilva')
    df = df.replace('Bruno Gustavo da Silva', 'BrunoGustavo DaSilva')
    df = df.replace('Johnny Munoz Jr.', 'Johnny MunozJr')
    df = df.replace('Abdul Razak Alhassan', 'AbdulRazak Alhassan')
    df = df.replace('Marcos Rogerio de Lima', 'MarcosRogerio DeLima')
    df = df.replace('Dricus Du Plessis', 'Dricus DuPlessis')
    df = df.replace('Jack Della Maddalena', 'Jack DellaMaddalena')
    df = df.replace('Maheshate', 'Maheshate Maheshate')
    df = df.replace('Rafael Dos Anjos', 'Rafael DosAnjos')
    df = df.replace('Alessio Di Chirico', 'Alessio DiChirico')
    df = df.replace('Montana de La Rosa', 'Montana DeLaRosa')
    df = df.replace('Ovince St. Preux', 'Ovince St.Preux')
    df = df.replace('Doo Ho Choi', 'DooHo Choi')
    df = df.replace('Mayra Bueno Silva', 'Mayra BuenoSilva')
    df = df.replace('Lina Akhtar Lansberg', 'Lina AkhtarLansberg')
    df = df.replace('Elizeu Zaleski Dos Santos', 'Elizeu ZaleskiDosSantos')
    df = df.replace('Da Un Jung', 'DaUn Jung')
    df = df.replace('James Te Huna', 'James TeHuna')
    df = df.replace('Douglas Silva de Andrade', 'Douglas SilvaDeAndrade')
    df = df.replace('Anderson Dos Santos', 'Anderson DosSantos')
    df = df.replace('Antonio Rodrigo Nogueira', 'AntonioRodrigo Nogueira')
    df = df.replace('Ji Yeon Kim', 'JiYeon Kim')
    df = df.replace('Jin Soo Son', 'JinSoo Son')
    df = df.replace('Yorgan de Castro', 'Yorgan DeCastro')
    df = df.replace('Phil de Fries', 'Phil DeFries')
    df = df.replace('Junior Dos Santos', 'Junior DosSantos')

    df = df.replace('Event props', 'Props')

    #get only rows with one space (first and last name)
    df2 = df[df['Name'].apply(lambda x: True if len(str(x).split()) == 2 else False)]

    df2 = df2.dropna(how='all').reset_index()

    #print(df2)


    oddsDF = pd.DataFrame(columns=['Event', 'Date', 'Name', 'Opponent', '5D_odds', 'Ref_odds' ])

    oddsDF['5D_odds'] = df2[['5D']]
    oddsDF['Ref_odds'] = df2[['Ref']]
    oddsDF['Name'] = df2[['Name']]
    oddsDF['Date'] = date
    oddsDF['Event'] = event

    for i in range(len(oddsDF)):
        #print(oddsDF.iloc[i]['Opponent'])
        if i % 2:
            oddsDF.at[i, 'Opponent'] = oddsDF.iloc[i-1]['Name']
        else:
            oddsDF.at[i, 'Opponent'] = oddsDF.iloc[i+1]['Name']
    
    oddsDF = oddsDF[oddsDF[['5D_odds', 'Ref_odds']].notnull().sum(1).ge(2)]

    return oddsDF, event

#odds, event = scrape_odds('https://www.bestfightodds.com/events/ufc-263-adesanya-vs-vettori-2-2115')

i=0
broken_urls = []


for url in df['event_url'][250:]:

    
    try:
        odds, event = scrape_odds(url)

        agg_odds_df = pd.concat([agg_odds_df, odds])
        print('Successfully appended odds data for ' + event)

    except: 
        print('Failed to capture table from ' + url)
        broken_urls.append(url)

    i=i+1
    
print(f'There were a total of {str(len(broken_urls))} broken urls out of {str(i)} total. ({str(len(broken_urls)/i*100)}%)')

#print(broken_urls)

print(f'Successfully appended {str(len(agg_odds_df))} fighter odds instances to dataset.')

agg_odds_df.to_csv('aggregate_odds2.csv')

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