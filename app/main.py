from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import cities,users

app = FastAPI(title="LIA Platform - Demo")

# Plug in the routers, so their endpoints become part of the app
app.include_router(cities.router)
app.include_router(users.router)

@app.on_event("startup")
async def on_startup():
     # Creates the tables in Postgres if they don't exist yet.
     # (For a demo only. In the real project we'd use Alembic migrations.)
     async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def homepage():
     return {"message": "Welcome to the LIA Platform API"}