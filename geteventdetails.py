import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website that contains the event links
url = 'http://ufcstats.com/statistics/events/completed?page=all'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the div that contains the event links
event_div = soup.find('tbody')

# Extract the URLs for each event link
event_urls = []
for event_link in event_div.find_all('a'):
    event_urls.append(event_link['href'])

# Create an empty pandas DataFrame to store the scraped data
event_df = pd.DataFrame()

# Loop through each URL in the event_urls list
for eventnum, url in enumerate(event_urls[0:5]):
    # Send a GET request to the event page
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    #get event name, date, and location
    eventname = soup.find('span', {'class':'b-content__title-highlight'}).text.strip()
    eventdate = soup.find('li', {'class' : 'b-list__box-list-item'}).text.strip().replace('Date:', '').replace(' ','')[2:]
    eventlocation = soup.find_all('li', {'class' : 'b-list__box-list-item'})[1].text.strip().replace('Location:', '').replace(' ','')[3:]

    #get weight class, method of victory, win round, and time
    # Extract the table containing the event data
    table = soup.find('table', {'class': 'b-fight-details__table'})

    #get list of fight urls
    fighturls = []
    fighttags = soup.find_all('a',{'class':'b-flag b-flag_style_green'}, href=True)
    for a in fighttags:
        fighturls.append(a['href'])

    #loop through all urls to scrape detailed fight data
    for fightnum, fighturl in enumerate(fighturls):
        response = requests.get(fighturl)

        fighter_names = []
        labels = []
        values = []

        soup = BeautifulSoup(response.content, 'html.parser')

        #get fighter names
        fighters = soup.find_all('div', {'class':'b-fight-details__person'})
        for fighter in fighters:
            if fighter.find('i', {'class':'b-fight-details__person-status_style_green'}):
                winner_name = fighter.find('a').text.strip()
            if fighter.find('i', {'class':'b-fight-details__person-status_style_gray'}):
                loser_name = fighter.find('a').text.strip()
        fighter_names.append(winner_name)
        fighter_names.append(loser_name)

        #print out winner and loser namses
        print(fighter_names)

        details = soup.find('div', {'class':'b-fight-details__fight'})

        details_list = []

        for deet in details.find_all('i'):
            details_list.append(deet.text.strip().strip())

        wtclass = details_list[0].replace('Bout', '').strip()
        method = details_list[3]
        winround = details_list[4].replace('Round:', '').replace(' ','').replace('\n', '')
        wintime = details_list[6].replace('Time:', '').replace(' ','').replace('\n', '')
        referee = details_list[10].replace('Referee:', '').replace('\n', '').strip()

        #print out fight details
        print([wtclass, method, winround, wintime, referee])

        tables = soup.find_all('table') 
        #### There are 4 tables total, two are used now ([0,2]), 
        ## but the other two may be useful later, 
        #### [1,3] contain detailed strike summarized by round 

        #scrape first table
        row0 = tables[0].find_all('tr',{'class':'b-fight-details__table-row'})[0]
        for col in row0.find_all('th', {'class':'b-fight-details__table-col'}):
            labels.append(col.text.strip())
        row1 = tables[0].find_all('tr',{'class':'b-fight-details__table-row'})[1]
        for c in row1.find_all('p',{'class':'b-fight-details__table-text'}):
            values.append(c.text.strip())


        labels2 = []
        values2 = []

        #scrape third table
        row0 = tables[2].find_all('tr',{'class':'b-fight-details__table-row'})[0]
        for col in row0.find_all('th', {'class':'b-fight-details__table-col'}):
            labels2.append(col.text.strip())
        row1 = tables[2].find_all('tr',{'class':'b-fight-details__table-row'})[1]
        for c in row1.find_all('p',{'class':'b-fight-details__table-text'}):
            values2.append(c.text.strip())

        #combine data excluding redundant columns [0:2]
        values =  values + values2[6:] 

        #break up values by fighter and add victory column
        evencols = values[0:][::2]
        oddcols = values[1:][::2]
        if evencols[0] == winner_name:
            evencols = evencols + ['won'] 
            oddcols = oddcols + ['lost'] 
        elif oddcols[0] == winner_name:
            oddcols = oddcols + ['won'] 
            evencols = evencols + ['lost'] 

        #organize data
        labels = ['EventNo', 'EventName', 'EventLoc', 'FightNo'] + labels + labels2[3:] + ['Outcome','WeightClass','Method','WinRound','WinTime','Referee']
        evencols = [eventnum, eventname, eventlocation, fightnum ] + evencols + [wtclass, method, winround, wintime, referee]
        oddcols = [eventnum, eventname, eventlocation, fightnum ] + oddcols + [wtclass, method, winround, wintime, referee]

        #add to df and concatenate 
        newdf = pd.DataFrame(columns=labels)
        newdf.loc[0] = evencols
        newdf.loc[1] = oddcols
        event_df = pd.concat([event_df, newdf])

print(event_df)

# Write the event_data DataFrame to a CSV file
event_df.to_csv('ufc_fight_outcomes.csv', index=False)