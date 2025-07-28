from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSettingsDTO(BaseModel):
    id: Optional[int] = None
    user_id: str
    address: str = ""
    street: str = ""
    passport_code: str = ""
    language: str = "en"
    timezone: str = "UTC"
    push_notifications: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserSettingsUpdateDTO(BaseModel):
    address: Optional[str] = None
    street: Optional[str] = None
    passport_code: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    push_notifications: Optional[bool] = None

class UserSettingsCreateDTO(BaseModel):
    user_id: str
    address: str = ""
    street: str = ""
    passport_code: str = ""
    language: str = "en"
    timezone: str = "UTC"
    push_notifications: bool = True 