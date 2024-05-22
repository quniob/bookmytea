from redis import Redis
import bookmytea_core.app.db.settings as settings

r = Redis(host='localhost', port=6379, db=0, decode_responses=True)
r.set("AUTO_CONFIRM", settings.AUTO_CONFIRM)


def get_auto_confirm() -> bool:
    return r.get("AUTO_CONFIRM") == 'true'

