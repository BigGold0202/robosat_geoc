from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class task(Base):
    task_id = Column(Integer, primary_key=True)
    extent = Column(String(256))
    user_id = Column(String(50))
    state = Column(Integer, default=1)
    status = Column(Integer, default=1)
