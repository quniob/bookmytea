import datetime
from datetime import timedelta

from bookmytea_core.app.db.models import *
from pony.orm import db_session


@db_session
def get_rooms() -> list[dict]:
    return [room.to_dict() for room in Room.select()]


@db_session
def add_room(name, desc) -> None:
    Room(name=name, desc=desc)


@db_session
def add_table(room_id, number, capacity, value) -> None:
    Table(room=Room[room_id], number=number, capacity=capacity, value=value)


@db_session
def create_booking(room_id, table_id, user_id, with_master, additional_info, start_time, duration) -> bool:
    table = Table[table_id]
    user = User[user_id]
    Booking(tables=table, user=user, with_master=with_master, additional_info=additional_info, start_time=start_time,
            end_time=start_time + timedelta(hours=duration),
            status='pending', confirmation_deadline=start_time)
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
        query = select(b for b in Booking if table in b.tables)
        query2 = query.filter(lambda b: b.start_time < end_time and b.end_time > start_time)
        bookings = query2.first()
        if bookings is None:
            available_tables.append(table)
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


if __name__ == '__main__':
    #    print(add_room('test1', 'test1'))
    #    print(add_table(1, 1, 1, 1))
    #    print(create_booking(1, 1, 1, True, 'additionalInfo', datetime.now() + timedelta(hours=12), 1))
    print(get_bookings())
