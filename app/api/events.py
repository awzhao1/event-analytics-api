from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Event
from app.schemas.event import EventCreate

# creates the router
router = APIRouter(prefix="/events", tags=["events"])

# handles sqlalchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
