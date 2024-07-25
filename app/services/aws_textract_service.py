import boto3
import os
from dotenv import load_dotenv

load_dotenv()


def get_textract_client():
    return boto3.client(
        'textract',
        region_name=os.getenv('AWS_REGION_NAME'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )


def analyze_document(file_path):
    client = get_textract_client()
    with open(file_path, 'rb') as document:
        response = client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['TABLES', 'FORMS']
        )
    return response
