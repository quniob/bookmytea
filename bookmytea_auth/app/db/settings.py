import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PONY_PROVIDER = os.environ.get("PONY_PROVIDER")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE")
JWT_SECRET = "x29803ytj237xt601wer1-iojwet"
