from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable= False )
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))  #optional
    password_hash = Column(String(255))
    city_id = Column(Integer, ForeignKey("cities.id"), nullable= False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )