from typing import List, Any, Optional
from datetime import datetime
from ninja import Schema
from pydantic import EmailStr


class QueueDetailSchema(Schema):
    id: int
    name: str


class QueueCreateSchema(Schema):
    id: int


class QueueUpdateSchema(Schema):
    name: str
    alphabet: str


class EntryCreateSchema(Schema):
    queue: int


class EntryDetailSchema(Schema):
    name: str
    status: str


class EntryListSchema(Schema):
    id: int
    name: str
    status: str
