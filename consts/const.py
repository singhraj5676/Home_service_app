import os

from dotenv import load_dotenv

load_dotenv()

RDS_HOST = os.getenv("RDS_HOST")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_PORT = os.getenv("RDS_PORT")
RDS_DATABASE = os.getenv("RDS_DATABASE")
DATABASE_URL = os.getenv("DATABASE_URL")
EMAIL_USER= os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SECRET_KEY =  os.getenv('SECRET_KEY')
ALGORITHM =  os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES =  os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_DAYS =  os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')