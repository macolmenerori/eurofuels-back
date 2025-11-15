import json
import pandas as pd
import boto3
import os
from io import BytesIO

def lambda_handler(event, context):
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    FILE_NAME = os.environ.get('FILE_NAME')
    EXCEL_URL = os.environ.get('EXCEL_URL')

    try:
        # Retrieve and parse the Excel file
        prices_raw = pd.read_excel(
            EXCEL_URL, 
            sheet_name=0, 
            header=1, 
            usecols='A:C', 
            names=['country', 'gasoline', 'diesel'], 
            nrows=27, 
            dtype=str, 
            engine='openpyxl'
        )

        # Convert to JSON
        prices_list = prices_raw.to_dict(orient='records')
        json_content = json.dumps(prices_list, indent=2, ensure_ascii=False)
        prices_raw.to_json(orient='records', force_ascii=False)

        # Upload to S3
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_NAME,
            Body=json_content,
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Fuel prices successfully updated',
                'file': FILE_NAME,
                'records': len(prices_list)
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating fuel prices',
                'error': str(e)
            })
        }
