from pony.orm import Database, Required, PrimaryKey
import bcrypt

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


db.bind(provider='sqlite', filename='auth.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
