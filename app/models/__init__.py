# This file makes the models folder a Python package.
# It collects all database models in one place.
# This lets us import models easily, for example:
# from models import City, User

# Import the common SQLAlchemy Base class
from app.models.base import Base

# Import database models so SQLAlchemy knows about them
from app.models.city import City
from app.models.user import User

# Define which names are officially exposed by the models package
__all__ = ["Base", "City", "User"]