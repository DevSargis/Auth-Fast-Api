from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from users.models.enums.user_role import UserRole

class UserTransformDTO(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = UserRole.USER.value
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserSearchResultDTO(BaseModel):
    users: List[UserTransformDTO]
    total_count: int

class UserMetadataServiceDTO(BaseModel):
    public_metadata: Dict[str, Any] = {}
    private_metadata: Dict[str, Any] = {}

class ServiceResponseDTO(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None 