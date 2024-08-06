import os

from dotenv import load_dotenv

load_dotenv()

RDS_HOST = os.getenv("RDS_HOST")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_PORT = os.getenv("RDS_PORT")
RDS_DATABASE = os.getenv("RDS_DATABASE")
