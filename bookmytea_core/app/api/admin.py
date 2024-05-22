import datetime as datetime
from typing import Optional

import fastapi_jsonrpc as jsonrpc
import bookmytea_core.app.db.db as db
from pydantic import BaseModel

admin_entrypoint = jsonrpc.Entrypoint('/api/v1/jsonrpc/admin')


class Booking(BaseModel):
    id: int
    user: int
    with_master: bool
    additional_info: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    status: str
    confirmation_deadline: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime


class BookingFilter(BaseModel):
    user: Optional[int] = None
    with_master: Optional[bool] = None
    status: Optional[str] = None


@admin_entrypoint.method()
def list_bookings(filter: BookingFilter) -> list[Booking]:
    rows = db.get_bookings()
    bookings = []
    for row in rows:
        if filter.user is not None and row['user'] != filter.user:
            continue
        if filter.with_master is not None and row['with_master'] != filter.with_master:
            continue
        if filter.status is not None and row['status'] != filter.status:
            continue
        bookings.append(Booking(**row))
    return bookings


@admin_entrypoint.method()
def cancel_booking(booking_id: int) -> bool:
    return db.cancel_booking(booking_id)


@admin_entrypoint.method()
def confirm_booking(booking_id: int) -> bool:
    return db.confirm_booking(booking_id)