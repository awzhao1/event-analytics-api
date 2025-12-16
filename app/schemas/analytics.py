from pydantic import BaseModel


class EventSummary(BaseModel):
    event_type: str
    count: int
