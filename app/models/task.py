from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class task(Base):
    task_id = Column(Integer, primary_key=True)
    job_id = Column(Integer)
    extent = Column(String(256))
    user_id = Column(String(50))
    area_code = Column(String(50))
    state = Column(Integer, default=1)
    status = Column(Integer, default=1)
    handler = Column(String(255))
    created_at = Column(DateTime)
    end_at = Column(DateTime)