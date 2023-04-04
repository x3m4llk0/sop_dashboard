import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class Script(Base):
    __tablename__ = "script"
    script_id = Column(Integer, primary_key=True, unique=True)
    script_name = Column(Integer, default="NotGameName")
    script_state = Column(Integer, default=False)

    def __init__(self, script_id: int, script_name: str, script_state: int = 0):
        self.script_id = script_id
        self.script_name = script_name
        self.script_state = script_state



class Quarter(Base):
    __tablename__ = "db_api_quarter"
    id = Column(Integer, primary_key=True, autoincrement=False)
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)