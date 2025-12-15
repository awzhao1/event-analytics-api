from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

app = FastAPI(title="Event Analytics API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
