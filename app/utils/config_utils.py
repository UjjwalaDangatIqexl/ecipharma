import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
    MONGO_URI = os.getenv('MONGO_URI')
    MAIL_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
    MAIL_PORT = 587
    MAIL_USERNAME = 'ujjwala.dangat@gmail.com'
    MAIL_PASSWORD = 'izwwjiewvtdovzsu'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

