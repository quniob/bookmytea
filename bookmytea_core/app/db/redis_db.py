from redis import Redis
import app.db.settings as settings

r = Redis(host=settings.REDIS_HOST, port=6379, db=0, decode_responses=True)
r.set("AUTO_CONFIRM", settings.AUTO_CONFIRM)


def get_auto_confirm() -> bool:
    return r.get("AUTO_CONFIRM").lower() == 'true'


def toggle_auto_confirm() -> None:
    if get_auto_confirm():
        r.set("AUTO_CONFIRM", "false")
    else:
        r.set("AUTO_COMFIRM", "true")


def check_telegram_user(user_id):
    return r.get(user_id)