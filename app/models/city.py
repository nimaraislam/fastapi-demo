from sqlalchemy  import Column, Integer, String, Float
from app.models import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key= True)
    name = Column(String(225), unique=True, nullable=False)
    region = Column(String(255), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
