from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime


class RoomBase(BaseModel):
    description: str
    price: float
    location: str
    amenities: List[str] = []
    beds: int = 1
    max_guests: int = 2
    room_type: str = "standard"
    has_kitchen: bool = False
    available_from: Optional[date] = None
    available_to: Optional[date] = None


class RoomCreate(RoomBase):
    embedding: List[float]  # Provided on creation (via embedding step)


class RoomOut(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
