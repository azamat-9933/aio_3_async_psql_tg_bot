import os
from dotenv import load_dotenv

# Загружаю
load_dotenv()

TOKEN = os.getenv('TOKEN')

DB_DRIVER = os.getenv('DB_DRIVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

FEEDBACK_CHANNEL = os.getenv('FEEDBACK_CHANNEL')

DB_URI = os.getenv('DB_URI')