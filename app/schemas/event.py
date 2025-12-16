from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime

# separates api input from db models
class EventCreate(BaseModel):
    user_id: UUID
    event_type: str
    timestamp: Optional[datetime] = None
    event_metadata: Optional[Dict] = None
