import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PONY_PROVIDER = os.getenv("PONY_PROVIDER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
AUTO_CONFIRM = os.getenv("AUTO_CONFIRM")
REDIS_HOST = os.getenv("REDIS_HOST")