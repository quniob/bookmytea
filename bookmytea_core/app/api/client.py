import datetime as datetime
from typing import Optional
from uuid import UUID

import fastapi_jsonrpc as jsonrpc
import bookmytea_core.app.db.db as db
from pydantic import BaseModel


class Table(BaseModel):
    id: int
    number: int
    capacity: int
    value: float


class Booking(BaseModel):
    id: int
    with_master: bool
    additional_info: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    status: str
    deadline: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime


class BookingRequest(BaseModel):
    room_id: int
    table_id: int
    user_id: str
    teaType: str
    additionalInfo: str
    time: str
    duration: int


class BookingResponse(BaseModel):
    table_id: int
    result: bool


class Room(BaseModel):
    id: int
    name: str
    desc: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: UUID
    email: str
    telegram: str | None


client_entrypoint = jsonrpc.Entrypoint('/api/v1/jsonrpc/client')


@client_entrypoint.method()
def get_rooms() -> list[Room]:
    rooms = db.get_rooms()
    return [Room(**room) for room in rooms]


@client_entrypoint.method()
def get_available_tables(room_id: int, date: datetime.date, start_time: datetime.time, duration: int) -> list[Table]:
    result = db.get_available_tables(room_id, date, start_time, duration)
    return result


@client_entrypoint.method()
def book_tables(tables: list[BookingRequest]) -> list[BookingResponse]:
    result = []
    for i in tables:
        book = db.create_booking(i.room_id, i.table_id, i.user_id, i.teaType, i.additionalInfo, i.time, i.duration)
        result.append(BookingResponse(table_id=i.table_id, result=book))
    return result


@client_entrypoint.method()
def get_booking_status(booking_id: int) -> str:
    return db.get_booking_status(booking_id)


@client_entrypoint.method()
def get_user(user_id: str) -> User:
    user = db.get_user(UUID(user_id))
    return User(**user)


@client_entrypoint.method()
def add_user(uuid: UUID, email: str) -> bool:
    return db.add_user(uuid, email)
