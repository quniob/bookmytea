from redis import Redis
from bookmytea_integrations.app import settings

r = Redis(host=settings.REDIS_HOST, port=6379, db=0, decode_responses=True)
