from jose import jwt
from uuid import UUID
from datetime import datetime, timedelta
from pony.orm import db_session
from bookmytea_auth.app.db.db import User, hash_password, check_password
from bookmytea_auth.app.db import settings


@db_session
def register(email: str, password: str, uuid: str):
    hashed_password = hash_password(password).decode('utf-8')
    existing_user = User.get(email=email)
    if not existing_user:
        admin = email == settings.ADMIN_MAIL
        User(id=UUID(uuid), email=email, password=hashed_password, admin=admin)
        return True
    else:
        return False


@db_session
def login(email, password):
    user = User.get(email=email)
    if user and check_password(user.password, password):
        payload = {
            'uuid': str(user.id),
            'admin': str(user.admin),
            'exp': datetime.now() + timedelta(hours=6)
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
        return token
    else:
        return None


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        return {'user_id': payload['uuid'], 'admin': payload['admin']}
    except jwt.ExpiredSignatureError:
        return None
