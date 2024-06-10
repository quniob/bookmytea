import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_HOST = os.getenv("REDIS_HOST")
BOT_TOKEN = os.getenv("BOT_TOKEN")