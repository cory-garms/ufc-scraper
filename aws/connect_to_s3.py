import boto3
import os
from dotenv import load_dotenv
import logging
from botocore.exceptions import ClientError
import pandas as pd
from collections import Counter
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
        object_name = os.path.basename(file_name)

    try:
        response = s3.Bucket(bucket).upload_file(filename, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# ### example use to upload and/or update a file in s3 bucket
# response = upload_file_to_S3('../csv/ufc_fighter_data.csv','fighter.database', 'ufcfighterdata')
# print(response)

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

    #delete bad urls from list
    df.drop(df.index[[2359, 2360]], inplace=True)
    
    d = df['URL']

    non_unique = [k for (k,v) in Counter(d).items() if v > 1]

    #print(non_unique)

    #df.drop(df.index[[2359, 2360]], inplace=True)

    #print(df.loc[df['URL'].isin(non_unique)])

    return df['URL'].unique()


existingURLs = get_existing_fighter_urls('./s3_ufcfighterdata.csv')



# print(len(existingURLs))

def look_for_new_urls(oldurls):
    active_url = 'https://www.ufc.com/athletes/all?gender=All&search=&filters%5B0%5D=status%3A23&page={str(i)}'
    active_total = 95

    pages = range(1, active_total)

    urllist = []
    for i in pages:
        urllist.append(f'https://www.ufc.com/athletes/all?gender=All&page={str(i)}')

    newurls = []

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
        if homeurl not in oldurls:
            newurls.append('https://www.ufc.com' + homeurl['href'])


    return newurls




output = look_for_new_urls(existingURLs)

print(output)