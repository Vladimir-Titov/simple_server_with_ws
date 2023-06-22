from typing import Optional

from pydantic import BaseModel

from app.models.common import EventType


class Message(BaseModel):
    event_type: EventType
    from_: str
    payload: Optional[dict] = None
