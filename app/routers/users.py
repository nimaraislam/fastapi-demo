from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import City, User
from app.schemas import UserCreate, UserOut

# Every endpoint in this file starts with /users
# and is grouped under "users" on the /docs page
router = APIRouter(prefix="/users", tags=["users"])

@router.post("",response_model=UserOut)
async def create_user(user: UserCreate, db : AsyncSession = Depends(get_db)):
     # user: FastAPI checks the incoming JSON against the UserCreate schema
     # db:   FastAPI calls get_db() and gives us a session from the connection pool

    # 1. The city must exist, because city_id is a foreign key
    city=await db.get(City, user.city_id)
    if not city:
        raise HTTPException(status_code=400, detail="City does not exist")

    # 2. The email must not be registered already
    existing = await db.execute(select(User).where(User.email == user.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 3. Create the database object from the validated data and save it
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) # reload so we get id, created_at, etc.

    # 4. Returned through UserOut, so password_hash is never included
    return new_user

@router.get("", response_model=list[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserOut)
async def get_a_user(user_id : int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user