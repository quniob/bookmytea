import datetime
import uuid
from datetime import timedelta, time

from bookmytea_core.app.db.models import *
from pony.orm import db_session
from bookmytea_core.app.db.redis_db import get_auto_confirm

opening_time = time(10, 0)
closing_time = time(21, 0)


@db_session
def get_rooms() -> list[dict]:
    return [room.to_dict() for room in Room.select()]


@db_session
def add_room(id, name, desc, image_url) -> None:
    if id:
        Room(id=id, name=name, desc=desc, image=image_url)
    else:
        Room(name=name, desc=desc, image=image_url)


@db_session
def add_table(room_id, number, capacity, value) -> None:
    Table(room=Room[room_id], number=number, capacity=capacity, value=value)


@db_session
def create_booking(room_id, table_id, user_id, with_master, additional_info, start_time, duration) -> bool:
    table = Table[table_id]
    user = User[user_id]
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if get_auto_confirm():
        status = "confirmed"
    else:
        status = "pending"
    Booking(table=table, user=user, with_master=with_master, additional_info=additional_info, start_time=start_time,
            end_time=start_time + timedelta(hours=duration),
            status=status, confirmation_deadline=start_time)
    return True


@db_session
def get_booking_status(booking_id) -> str:
    return Booking[booking_id].status


@db_session
def get_available_tables(room_id, booking_date, start_time, duration):
    start_time = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end_time = start_time + timedelta(hours=duration)
    available_tables = []
    room = Room[room_id]
    for table in room.tables:
        bookings = table.booking.select()
        bookings = [booking for booking in bookings if booking.start_time <= start_time <= booking.end_time or
                    booking.start_time <= end_time <= booking.end_time or
                    start_time <= booking.start_time <= end_time or start_time <= booking.end_time <= end_time]
        bookings = [booking for booking in bookings if booking.status != 'cancelled' or booking.status != 'completed']
        if not bookings:
            available_tables.append(table.to_dict())
    return available_tables


@db_session
def get_bookings() -> list[dict]:
    return [booking.to_dict() for booking in Booking.select()]


@db_session
def cancel_booking(booking_id) -> bool:
    booking = Booking[booking_id]
    if booking is None or booking.status == 'completed':
        return False
    booking.status = 'cancelled'
    return True


@db_session
def confirm_booking(booking_id) -> bool:
    booking = Booking[booking_id]
    if booking is None or booking.status == 'completed':
        return False
    booking.status = 'confirmed'
    return True


@db_session
def add_user(uuid: UUID, email: str):
    User(id=uuid, email=email)
    return True


@db_session
def get_user(user_id):
    return User[user_id].to_dict()


if __name__ == '__main__':
    add_room(1, 'Самурай', 'Зал в стиле японского милитаризма', 'https://gcdnb.pbrd.co/images/lIemefZGSwZo.png')
    add_room(2, "Дзен", "Светлый зал для спокойных чаепитий", "https://i.imgur.com/VX2JewI.png")
    add_table(1, 1, 4, 200)
    add_table(1, 2, 4, 200)
    add_table(1, 3, 4, 200)
    add_table(1, 4, 6, 350)
    add_table(2, 1, 4, 200)
    add_table(2, 2, 4, 200)
    add_table(2, 3, 4, 200)
    print(get_rooms())
    print(get_available_tables(1, "2021-09-01", "12:00:00", 2))