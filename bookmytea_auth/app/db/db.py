from pony.orm import Database, Required, PrimaryKey
import bcrypt
from bookmytea_auth.app.db import settings
from uuid import UUID

db = Database()


class User(db.Entity):
    id = PrimaryKey(UUID)
    email = Required(str, unique=True)
    password = Required(str)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


db.bind(provider=settings.PONY_PROVIDER, user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_HOST, database=settings.POSTGRES_DATABASE,
        port=settings.POSTGRES_PORT)
db.generate_mapping(create_tables=True)
