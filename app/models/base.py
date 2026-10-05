from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):  #Base = foundation for all database models.
    pass

#Base is the parent class for all our SQLAlchemy database models. 
#It tells SQLAlchemy that classes like City, User, or Job represent database tables.
#We create Base from SQLAlchemy’s DeclarativeBase. Then all our database models inherit from Base, so SQLAlchemy knows they are ORM models.