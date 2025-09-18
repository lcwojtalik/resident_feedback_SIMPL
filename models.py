from pydantic import BaseModel, field_validator
from datetime import date

class Assignment(BaseModel):
    date: date
    attending_name: str
    resident_name: str
    service: str | None = None
    room: str | None = None

    @field_validator('attending_name', 'resident_name')
    @classmethod
    def strip_names(cls, v: str) -> str:
        return v.strip()

class Attending(BaseModel):
    attending_name: str
    email: str
    phone: str | None = None
