import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

logger = logging.getLogger('logger')
Base = declarative_base()

class DataBase:
    _engine = None
    _SessionFactory = None

    @classmethod
    def initialize(cls, database_url):
        if not cls._engine:
            cls._engine = create_engine(database_url, echo=True)
            cls._SessionFactory = sessionmaker(bind=cls._engine)

    @classmethod
    def get_session(cls):
        if not cls._SessionFactory:
            raise Exception("Database not initialized. Call initialize() first.")
        return scoped_session(cls._SessionFactory)

    @classmethod
    def create_all_tables(cls):
        if not cls._engine:
            raise Exception("Database not initialized. Call initialize() first.")
        Base.metadata.create_all(cls._engine)

    @classmethod
    def remove_session(cls):
        if cls._SessionFactory:
            cls._SessionFactory.remove()