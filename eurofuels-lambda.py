import boto3
import json
import os
import pandas as pd

def lambda_handler(event, context):
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    FILE_NAME = os.environ.get('FILE_NAME')

    prices_raw = pd.read_excel('http://energy.ec.europa.eu/document/download/264c2d0f-f161-4ea3-a777-78faae59bea0', 0, header=1, usecols='A:C', names=['country', 'gasoline', 'diesel'], nrows=27, dtype=str, engine='openpyxl')

    prices_JSON = prices_raw.to_json(orient='records', force_ascii=False)

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    json_content = json.dumps(prices_JSON, indent=2)

    s3.put_object(Bucket=BUCKET_NAME, Key=FILE_NAME, Body=json_content)
    return {
        'statusCode': 200,
        'body': json.dumps('eurofuels data successfully uploaded to S3')
    }
