from data.database import Base
from sqlalchemy import Column, Integer, String
from enum import Enum

class UserState(Enum):
    START = 1
    MANUFACTURER = 2
    MODEL = 3
    YEAR = 4
    PRICE = 5
    KM = 6

class UserFirstChoice(Enum):
    SEARCH_CAR = 1
    STATISTICS = 2
    CAR_DETAILS = 3

class User(Base):
    __tablename__ = 'user'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_state = Column(Integer)
    user_first_choice = Column(Integer)
    manufacturer = Column(Integer)
    model = Column(Integer)
    year = Column(String)
    price = Column(String)
    km = Column(String)