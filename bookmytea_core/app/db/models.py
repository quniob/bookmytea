from datetime import datetime, timedelta
from app.db import settings
from enum import Enum
from uuid import UUID

from pony.orm import Database, Required, Set, PrimaryKey, Optional, db_session, select

db = Database()


class BookingStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETE = 'complete'


class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    image = Optional(str, nullable=True, default=None)
    name = Required(str)
    desc = Optional(str)
    tables = Set("Table")


class User(db.Entity):
    id = PrimaryKey(UUID)
    email = Required(str)
    avatar = Optional(str, nullable=True, default="https://avatar.iran.liara.run/public/40")
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
    table = Required("Table")  # Нужно Required
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
        password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_HOST, database=settings.POSTGRES_DATABASE,
        port=settings.POSTGRES_PORT)
db.generate_mapping(create_tables=True)
