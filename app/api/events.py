from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Event
from app.schemas.event import EventCreate
from sqlalchemy import func
from app.schemas.analytics import EventSummary
from typing import List


# creates the router
router = APIRouter(prefix="/events", tags=["events"])

# handles sqlalchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creates an event in the database
# Dependency injection 
@router.post("/")
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(
        user_id=event.user_id,
        event_type=event.event_type,
        timestamp=event.timestamp,
        event_metadata=event.event_metadata,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {"id": db_event.id}

@router.get("/summary", response_model=List[EventSummary])
def event_summary(db: Session = Depends(get_db)):
    results =(
        db.query(
            Event.event_type,
            func.count(Event.id).label("count")
        )
        .group_by(Event.event_type)
        .all()
    )

    return [
        {"event_type": row.event_type, 'count': row.count}
        for row in results
    ]