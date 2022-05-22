from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Any


Base = declarative_base()


class DbClient:
    def __init__(self, connection: str, base: Any = Base):
        self.engine = create_engine(connection)
        self.Base = base
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Base.metadata.create_all(self.engine)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True, nullable=False)
    birth_year = Column(String(200), nullable=False)
    eye_color = Column(String(200), nullable=False)
    # films = Column(Text(), nullable=False)
    gender = Column(String(200), nullable=False)
    hair_color = Column(String(200), nullable=False)
    height = Column(String(200), nullable=False)
    homeworld = Column(String(100), nullable=False)
    mass = Column(String(100), nullable=False)
    name = Column(String(200), nullable=False)
    skin_color = Column(String(200), nullable=False)
    # species = Column(Text(), nullable=False)
    # starships = Column(Text(), nullable=False)
    # vehicles = Column(Text(), nullable=False)
