import os
import boto3
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION")
bucket_name = os.getenv("S3_BUCKET_NAME")

client = boto3.client(
    service_name = 's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name = region
)

response = client.list_buckets()

for bucket in response['Buckets']:
    print(bucket['Name'])