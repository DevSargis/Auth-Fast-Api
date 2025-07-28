from pydantic import BaseModel
from typing import Dict, Any, Optional
from users.models.enums.user_role import UserRole

class CurrentUserResponseDTO(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: str = UserRole.USER.value

class HealthCheckResponseDTO(BaseModel):
    status: str = "healthy"

class AdminRoleUpdateResponseDTO(BaseModel):
    message: str
    user_id: str
    updated_user: Optional[Dict[str, Any]] = None
