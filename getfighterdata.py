import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the UFC fighter list

range = range(1,95)
pagelist = []
for i in range:
    pagelist.append(i)

urllist = []
for i in pagelist:
    urllist.append(f'https://www.ufc.com/athletes/all?gender=All&search=&filters%5B0%5D=status%3A23&page={str(i)}')


names = []
nicknames = []
homeurls = []

for num, url in enumerate(urllist):

    print(f'getting fighter names and nickames from page {num} of {max(range)}')


    #url = urllist[0]

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table that contains the fighter data
    fighter_table = soup.find('div', {'class': 'item-list'})

    #print(fighter_table)

    for index,th in enumerate(fighter_table.find_all('a', {'class':'e-button--black'})):
        homeurls.append('https://www.ufc.com' + th['href'])

    for index, th in enumerate(fighter_table.find_all('span', {'class': 'c-listing-athlete__name'})):
        names.append(th.text.strip())

    for index, th in enumerate(fighter_table.find_all('span', {'class':'c-listing-athlete__nickname'})):
        nname = th.find('div',{'class':'field__item'})
        if nname:

            nicknames.append(nname.text.strip().replace('"',''))
        else:
            nicknames.append('None')

# print(names)
# print(nicknames)

d = {"Name" : names, "Nickname" : nicknames}

df = pd.DataFrame(d).drop_duplicates()
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

    for index, th in enumerate(soup.find_all('div', {'class': 'c-bio__field'})):

        label = th.find('div', {'class':'c-bio__label'}).text.strip()
        labels.append(label)
        
        value = th.find('div', {'class':'c-bio__text'}).text.strip()
        values.append(value)


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
    
    # if i < 1:
    #     df0[["Status","Birthplace","Style","Age","Height","Weight","OctagonDebut","Reach","LegReach"]] = df2

    # else:

    #     print(type(df0.iloc[i,]))
    #     print(type(df2))

    #     df3 = df2.combine_first(df0).reindex(df0.iloc[i,].index)


        # print(labels)
        # print(values)
        #print(df)
    




