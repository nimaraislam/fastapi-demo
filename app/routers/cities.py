from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import City
from app.schemas import CityCreate, CityOut

# All endpoints in this file start with /cities and are grouped under "cities" in /docs
router = APIRouter(prefix="/cities",tags=["cities"])

@router.post("",response_model=CityOut)
async def create_city(city: CityCreate, db: AsyncSession = Depends(get_db)):
    # city: FastAPI validates the incoming JSON against the CityCreate schema
    # db: FastAPI calls get_db() and gives us a database session from the connection pool

    # 1. Check whether the city already exists
    existing = await db.execute(select(City).where(City.name==city.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="City already exists")

    # 2. Create the database object from the validated data and save it
    new_city = City(**city.model_dump())  #.model_dump() is a Pydantic method that turns the object into a plain dictionary:
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)  # reload so we get the generated id

    # 3. Returned as CityOut (this is where from_attributes=True is used)
    return new_city

@router.get("", response_model= list[CityOut])
async def list_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).order_by(City.name))
    return result.scalars().all()
