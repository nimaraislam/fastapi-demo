import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,       # connections kept open per worker
    max_overflow=10,   # extra connections allowed under burst load
    pool_timeout=30,   # seconds to wait for a free connection
    pool_recycle=1800, # recycle connections every 30 min
    echo=False,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session