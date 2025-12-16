from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import User

# sqlalchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# returns a user object using http headers and dependency injection
def get_current_user(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.api_key == x_api_key).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user
