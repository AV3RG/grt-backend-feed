from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WebGLTable(Base):
    __tablename__ = "webgl_grt"
    User_id = Column(String, primary_key=True)
    Timestamp = Column(DateTime, primary_key=True, default=datetime.utcnow)
    Event = Column(String)
