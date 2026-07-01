import os
import boto3
from dotenv import load_dotenv

# Loading env variables 
load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION")
bucket_name = os.getenv("S3_BUCKET_NAME")

# Creating boto3 client
client = boto3.client(
    service_name = 's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name = region
)

# Printing bucket contents 
def print_bucket():
    response = client.list_buckets()

# Downloading a file
def download(bucket_name, object_name, file_name):
    client.download_file(bucket_name, object_name, file_name)

# Uploading a file
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
