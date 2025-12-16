from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.events import router as events_router

# # create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Analytics API")

# register the router
app.include_router(events_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
