import boto3
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
from collections import Counter
import csv
from datetime import datetime
from dotenv import load_dotenv
import json
import logging
import os
import pandas as pd
import requests

load_dotenv()

awsaccesskey = os.getenv("aws_access_key") 
awssecretkey = os.getenv("aws_secret_access_key")

# print(awsaccesskey)
# print(awssecretkey)

s3 = boto3.resource(
    service_name='s3',
    region_name='us-west-2',
    aws_access_key_id=awsaccesskey,
    aws_secret_access_key=awssecretkey
)

# ##list all buckets
# for bucket in s3.buckets.all():
#     print(bucket.name)

def upload_file_to_S3(filename, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(filename)

    try:
        response = s3.Bucket(bucket).upload_file(filename, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

### example use to upload and/or update a file in s3 bucket
response = upload_file_to_S3('../csv/ufc_fighter_data.csv','fighter.database', 'ufcfighterdata.csv')
print(response)

def get_file_from_S3(object_name, bucket, outputname):
    """Retrieve a file from S3 bucket

    :param object_name: S3 object name. 
    :param bucket: Bucket to upload to
    :param outputname: destination path with extension
    :return: True if file was uploaded, else False
    """
    try:
        s3.Bucket(bucket).download_file(object_name, outputname)
        return True

    except:
        return False

# ### example use to download a file from S3 bucket
# response = get_file_from_S3('ufcfighterdata', 'fighter.database', './s3_ufcfighterdata.csv')
# print(response)

def get_existing_fighter_urls(filename):
    #read in data
    df = pd.read_csv(filename)

    print(len(df['URL']))

    #delete bad urls from list
    df.drop(df.index[[2359, 2360]], inplace=True)
    
    d = df['URL']

    non_unique = [k for (k,v) in Counter(d).items() if v > 1]

    print(len(df['URL'].unique()))

    return df['URL'].unique()

# ### example use: get list of existing fighter urls
# existingURLs = get_existing_fighter_urls('./s3_ufcfighterdata.csv')
# print(existingURLs)

def find_new_urls(oldurls):
    active_url = 'https://www.ufc.com/athletes/all?gender=All&search=&filters%5B0%5D=status%3A23&page={str(i)}'
    active_total = 95

    pages = range(1, active_total)

    urllist = []
    for i in pages:
        urllist.append(f'https://www.ufc.com/athletes/all?gender=All&page={str(i)}')

    newurls = []

    for num, url in enumerate(urllist):
        print(f'getting fighter names and nickames from page {num+1} of {max(pages)}')

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
            url = 'https://www.ufc.com' + homeurl['href']

            if url not in oldurls:
                newurls.append(url)

    return newurls

#### example use: search for new fighter urls and write them out to csv
# output = find_new_urls(existingURLs[5:])
# print(output)
# with open('../csv/new_fighter_urls.csv', 'w', newline='') as myfile:
#      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#      wr.writerow(output)


def get_new_fighter_data(newurls, outfile):

    urls = open(newurls, "r")
    urllist = list(csv.reader(urls, delimiter=','))[0]
    urls.close()

    newdf = pd.DataFrame()


    for fighternum, u in enumerate(urllist[0:5]):
        
        # Send a GET request to the website
        response = requests.get(u)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            nickname = soup.find('p', {'class':'hero-profile__nickname'}).text.strip().replace('"', '')
        except:
            nickname = 'NA'
        name = soup.find('title').text.strip().replace('| UFC', '')


        labels = ['Name', 'Nickname', 'URL']
        values = [name, nickname, u]


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

    newdf.to_csv(outfile, index=False)

# ### example use: take in csv with list of new fighter urls and output csv with their scraped data
# get_new_fighter_data('../csv/new_fighter_urls.csv', '../csv/new_ufc_fighter_data.csv')

def merge_new_fighter_data(olddata, newdata):
    olddf = pd.read_csv(olddata)[5:].drop_duplicates(subset=['URL'], keep='last')
    newdf = pd.read_csv(newdata)

    outdf = pd.concat([olddf, newdf]).drop_duplicates(subset=['URL'], keep='last')
    outdf.to_csv('../csv/merged_ufc_fighter_data.csv')

    diff = len(outdf) - len(olddf)

    print(f'Added a total of {str(diff)} new fighters to the dataset')


# merge_new_fighter_data('../csv/ufc_fighter_data.csv', '../csv/new_ufc_fighter_data.csv')