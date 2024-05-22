from datetime import datetime, timedelta
from bookmytea_core.app.db import settings
from enum import Enum

from pony.orm import Database, Required, Set, PrimaryKey, Optional, db_session, select

db = Database()


class BookingStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    desc = Optional(str)
    tables = Set("Table")


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    telegram = Optional(str, nullable=True)
    bookings = Set("Booking")


class Table(db.Entity):
    id = PrimaryKey(int, auto=True)
    room = Required("Room")
    number = Required(int)
    capacity = Required(int)
    value = Required(float)
    booking = Set("Booking")


class Booking(db.Entity):
    id = PrimaryKey(int, auto=True)
    tables = Set("Table")
    user = Required("User")
    with_master = Required(bool, default=False)
    additional_info = Optional(str)
    start_time = Required(datetime)
    end_time = Required(datetime)
    status = Required(str, default='pending')
    confirmation_deadline = Required(datetime, default=lambda: datetime.utcnow() + timedelta(hours=6))
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


db.bind(provider=settings.PONY_PROVIDER, user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_HOST, database=settings.POSTGRES_DATABASE)
db.generate_mapping(create_tables=True)
