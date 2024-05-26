from os import environ
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

# Your enviroment variables
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
SCRAPING_KEY = environ.get('SCRAPING_KEY')