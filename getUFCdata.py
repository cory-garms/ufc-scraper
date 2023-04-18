bimport requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website that contains the event links
url = 'http://ufcstats.com/statistics/events/completed?page=all'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the div that contains the event links
#event_div = soup.find('div', {'class': 'b-statistics__search-results'})
event_div = soup.find('tbody')

# Extract the URLs for each event link
event_urls = []
for event_link in event_div.find_all('a'):
    event_urls.append(event_link['href'])

print(len(event_urls))

# Create an empty pandas DataFrame to store the scraped data
event_data = pd.DataFrame()

# Loop through each URL in the event_urls list
for url in event_urls[0:5]:
    # Send a GET request to the event page
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the event name and date from the page
    event_name = soup.find('h2', {'class': 'b-content__title'}).text
    event_date = soup.find('li', {'class': 'b-list__box-list-item'}).text

    # Extract the table containing the event data
    table = soup.find('table', {'class': 'b-fight-details__table'})

    # Convert the table to a pandas DataFrame
    df = pd.read_html(str(table))[0]

    # Add the event name and date as columns to the DataFrame
    df['event_name'] = event_name
    df['event_date'] = event_date

    # Append the DataFrame to the event_data DataFrame
    event_data = pd.concat([event_data, df])


# Write the event_data DataFrame to a CSV file
event_data.to_csv('ufc_event_data.csv', index=False)