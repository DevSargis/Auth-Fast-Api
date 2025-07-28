from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class AuthenticationResponseDTO(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    public_metadata: Dict[str, Any] = {}

class ClerkUserDTO(BaseModel):
    id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    public_metadata: Dict[str, Any] = {}
    private_metadata: Dict[str, Any] = {}
    created_at: str
    updated_at: str

class ClerkUserListDTO(BaseModel):
    users: List[ClerkUserDTO]
    total_count: int

class TokenValidationDTO(BaseModel):
    is_expired: bool
    is_valid: bool
    payload: Dict[str, Any] = {}

class UserMetadataDTO(BaseModel):
    public_metadata: Dict[str, Any] = {}
    private_metadata: Dict[str, Any] = {}


class RoleUpdateResponseDTO(BaseModel):
    id: str
    public_metadata: Dict[str, Any]
