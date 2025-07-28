from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserInfoDTO(BaseModel):
    user_id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserListResponseDTO(BaseModel):
    users: List[UserInfoDTO]
    total_count: int

class RoleUpdateRequest(BaseModel):
    role: str

class RoleUpdateResponse(BaseModel):
    user_id: str
    role: str
    success: bool

class UserSearchRequest(BaseModel):
    query: str

class UserMetadataResponse(BaseModel):
    public_metadata: Dict[str, Any]
    private_metadata: Dict[str, Any] 