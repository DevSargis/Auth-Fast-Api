from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserSettingsEntityDTO(BaseModel):
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

class UserSettingsListDTO(BaseModel):
    settings: List[UserSettingsEntityDTO]
    total_count: int

class RepositoryResponseDTO(BaseModel):
    success: bool
    message: str
    data: Optional[UserSettingsEntityDTO] = None

class RepositoryErrorDTO(BaseModel):
    error: str
    details: Optional[str] = None 