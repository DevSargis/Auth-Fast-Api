from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from fastapi import Request
from auth.models.dto.authentication_dto import (
    AuthenticationResponseDTO,
    ClerkUserDTO,
    ClerkUserListDTO,
    TokenValidationDTO,
    UserMetadataDTO,
    RoleUpdateResponseDTO
)

class AuthenticationService(ABC):
    @abstractmethod
    async def authenticate_user(self, request: Request) -> AuthenticationResponseDTO:
        """Authenticate user from request and return user details"""
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[ClerkUserDTO]:
        """Get user details by user ID"""
        pass
    
    @abstractmethod
    async def get_all_users(self) -> ClerkUserListDTO:
        """Get all users (admin only)"""
        pass
    
    @abstractmethod
    async def update_user_role(self, user_id: str, role: str) -> RoleUpdateResponseDTO:
        """Update user role (admin only)"""
        pass
    
    @abstractmethod
    async def is_token_expired(self, token: str) -> TokenValidationDTO:
        """Check if token is expired"""
        pass
    
    
    @abstractmethod
    async def get_user_metadata(self, user_id: str) -> Optional[UserMetadataDTO]:
        """Get user metadata"""
        pass 