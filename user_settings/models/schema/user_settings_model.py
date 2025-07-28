from sqlalchemy import Column, Integer, String, Boolean, DateTime
from configs.database_config import Base
from datetime import datetime

class UserSettingsModel(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    address = Column(String, default="", nullable=False)
    street = Column(String, default="", nullable=False)
    passport_code = Column(String, default="", nullable=False)
    language = Column(String, default="en", nullable=False)
    timezone = Column(String, default="UTC", nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 