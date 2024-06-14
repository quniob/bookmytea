from redis import Redis
from app import settings

r = Redis(host=settings.REDIS_HOST, port=6379, db=0, decode_responses=True)
