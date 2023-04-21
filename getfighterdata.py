import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the UFC fighter list
active_url = 'https://www.ufc.com/athletes/all?gender=All&search=&filters%5B0%5D=status%3A23&page={str(i)}'
inactive_url = 'https://www.ufc.com/athletes/all?gender=All&page={str(i)}'
active_total = 95
inactive_total = 257

pages = range(1,inactive_total)
pagelist = []
for i in pages:
    pagelist.append(i)

urllist = []
for i in pagelist:
    urllist.append(f'https://www.ufc.com/athletes/all?gender=All&page={str(i)}')

names = []
nicknames = []
homeurls = []

for num, url in enumerate(urllist):

    print(f'getting fighter names and nickames from page {num} of {max(pages)}')

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table that contains the fighter data
    fighter_table = soup.find('div', {'class': 'item-list'})
    for index, li in enumerate(fighter_table.find_all('li', {'class': 'l-flex__item'})):
        ## skip over empty fighter blocks
        if li.find('a') is None:
            continue
        homeurl = li.find('a', {'class': 'e-button--black'})
        homeurls.append('https://www.ufc.com' + homeurl['href'])
        name = li.find('span', {'class': 'c-listing-athlete__name'})
        names.append(name.text.strip())
        nickname = li.find('span', {'class':'c-listing-athlete__nickname'})
        if nickname is not None:
            nicknames.append(nickname.text.strip().replace('"',''))
        else:
            nicknames.append('None')

d = {"Name" : names, "Nickname" : nicknames}


df = pd.DataFrame(d) #.drop_duplicates()
print(len(df))
df['URL'] = homeurls

df0 = df.reset_index()

labels_list = []
values_list = []
names = []

newdf = pd.DataFrame()

for fighternum, u in enumerate(df['URL']):

    name = df0.iloc[fighternum]['Name']

    names.append(name)

    print(f'Fighter {fighternum}, {name}')
    
    # Send a GET request to the website
    response = requests.get(u)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    labels = []
    values = []

    ## Hero profile - only one such div exists
    value = soup.find('p', {'class': 'hero-profile__division-title'})
    labels.append('Division')
    if value is not None:
        values.append(value.text.strip())
    else:
        values.append('NA')

    value = soup.find('p', {'class': 'hero-profile__division-body'})
    labels.append('Record')
    if value is not None:
        values.append(value.text.strip())
    else:
        values.append('NA')

    for index, th in enumerate(soup.find_all('div', {'class': 'c-bio__field'})):
        label = th.find('div', {'class':'c-bio__label'}).text.strip()
        labels.append(label)
        
        value = th.find('div', {'class':'c-bio__text'}).text.strip()
        values.append(value)

    ## STRIKE / TAKEDOWN ACCURACY
    for index, dl in enumerate(soup.find_all('dl', {'class': 'c-overlap__stats'})):
        label = dl.find('dt', {'class': 'c-overlap__stats-text'}).text.strip()
        labels.append(label)

        value = dl.find('dd', {'class': 'c-overlap__stats-value'}).text.strip()
        values.append(value)

    ## STRIKES / TAKEDOWN INFO
    for index, div in enumerate(soup.find_all('div', {'class': 'c-stat-compare__group'})):
        label = div.find('div', {'class': 'c-stat-compare__label'}).text.strip()
        suffix = div.find('div', {'class': 'c-stat-compare__label-suffix'})
        if suffix is not None:
            label = " ".join([label, suffix.text.strip()])
        labels.append(label)

        value = div.find('div', {'class': 'c-stat-compare__number'})
        if value is not None:
            # get rid of weird % formatting
            value = value.text.strip().replace(" ", "").replace("\n", "")
            values.append(value)
        else:
            values.append("NA")

    ## STRIKES BY POSITION // WINS BY METHOD
    for index, div in enumerate(soup.find_all('div', {'class': 'c-stat-3bar c-stat-3bar--no-chart'})):
        for i, group in enumerate(div.find_all('div', {'class': 'c-stat-3bar__group'})):
            label = group.find('div', {'class': 'c-stat-3bar__label'}).text.strip()
            labels.append(label)

            value = group.find('div', {'class': 'c-stat-3bar__value'}).text.strip()
            values.append(value)

    ## STRIKES BY TARGET
    targets = []
    head_value = soup.find('text', {'id': 'e-stat-body_x5F__x5F_head_value'})
    labels.append("head total")
    targets.append(head_value)

    head_percent = soup.find('text', {'id': 'e-stat-body_x5F__x5F_head_percent'})
    labels.append("head percent")
    targets.append(head_percent)

    body_value = soup.find('text', {'id': 'e-stat-body_x5F__x5F_body_value'})
    labels.append("body total")
    targets.append(body_value)

    body_percent = soup.find('text', {'id': 'e-stat-body_x5F__x5F_body_percent'})
    labels.append("body percent")
    targets.append(body_percent)

    leg_value = soup.find('text', {'id': 'e-stat-body_x5F__x5F_leg_value'})
    labels.append("leg total")
    targets.append(leg_value)

    leg_percent = soup.find('text', {'id': 'e-stat-body_x5F__x5F_leg_percent'})
    labels.append("leg percent")
    targets.append(leg_percent)

    for target in targets:
        if target is not None:
            values.append(target.text.strip())
        else:
            values.append('NA')

    ## FIRST ROUND FINISHES
    label = "First Round Finishes"
    labels.append(label)
    value = "NA"
    hero_stats = soup.find_all('div', {'class', 'hero-profile__stat'})
    for index, hero_stat in enumerate(hero_stats):
        p_label = hero_stat.find('p', {'class', 'hero-profile__stat-text'}).text.strip()
        if p_label == label:
            value = hero_stat.find('p', {'class', 'hero-profile__stat-numb'}).text.strip()
    values.append(value)


    ## NEW
    df2 = pd.DataFrame(values).T

    for index, label in enumerate(labels):
        df2 = df2.rename(columns={index:label})

    newdf = pd.concat([newdf,df2])

    print(df2)

newdf['Name'] = names
print(names)

print(newdf)

df = pd.merge(df, newdf, on='Name')

print(df)

df.to_csv('ufc_fighter_data.csv', index=False)
    
