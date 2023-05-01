import boto3
import os
from dotenv import load_dotenv
import logging
from botocore.exceptions import ClientError
import pandas as pd

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
# print('Successful upload')

def get_file_from_S3(object_name, bucket, outputname):
    try:
        s3.Bucket(bucket).download_file(object_name, outputname)
        return('Successful Download')

    except:
        return('Unsuccessful Download')

### example use to download a file from S3 bucket
response = get_file_from_S3('ufcfighterdata', 'fighter.database', './s3_ufcfighterdata.csv')
print(response)

def get_existing_fighters(filename):
    df = pd.read_csv(filename)
    print(len(df['URL']))

    print(len(df['URL'].unique()))

    return df['URL'].unique()

existingURLs = get_existing_fighters('./s3_ufcfighterdata.csv')


# def get_new_urls(oldurls):

