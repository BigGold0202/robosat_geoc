from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class task_admin(Base):
    task_id = Column(Integer, primary_key=True)
    extent = Column(String(256))
    user_id = Column(String(50))
    area_code = Column(String(50))
    state = Column(Integer, default=1)
    status = Column(Integer, default=1)
    end_at = Column(DateTime)
    handler = Column(String(50), default=1)
    originalextent = Column(String(256))
    updated_at = Column(DateTime)
