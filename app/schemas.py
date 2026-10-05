from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

# ---------------------------------------------------------------
# What is a schema?
# A schema describes the shape of data going IN to and OUT of the API.
# It is NOT the database table (that's in app/models/).
# FastAPI uses schemas to:
#   1. validate incoming data automatically
#   2. control exactly which fields are returned to the client
#   3. generate the /docs page
# ---------------------------------------------------------------


# ----------------------------- CITY -----------------------------

class CityCreate(BaseModel):
    """Data the client SENDS when creating a city."""
    name: str                            # required
    region: str                          # required
    latitude: float | None = None        # optional (defaults to None)
    longitude: float | None = None       # optional (defaults to None)


class CityOut(CityCreate):
    """Data the API RETURNS for a city.
    Inherits all fields from CityCreate and adds the database-generated id."""
    id: int

    # Allows Pydantic to read from a SQLAlchemy object (city.name)
    # instead of only from a dictionary (city["name"]).
    model_config = ConfigDict(from_attributes=True)

# ----------------------------- USER -----------------------------

class UserCreate(BaseModel):
    """Data the client SENDS when registering.
    Note: no id, is_active, created_at or password_hash here, so the
    client cannot set those fields themselves."""
    name: str
    email: EmailStr                      # validated: must look like a real email
    phone: str | None = None             # optional
    city_id: int                         # must match an existing city's id

class UserOut(BaseModel):
    """Data the API RETURNS for a user.
    password_hash is deliberately left out, so it can never leak."""
    id: int
    name: str
    email: str
    phone: str | None
    city_id: int
    is_active: bool
    created_at: datetime

    # Same as above: lets Pydantic read from a SQLAlchemy User object.
    model_config = ConfigDict(from_attributes=True)