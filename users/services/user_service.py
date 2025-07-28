import os
import logging
from typing import Dict, Any, Optional, List
from auth.services.authentication_service import AuthenticationService
from auth.models.dto.authentication_dto import (
    ClerkUserDTO,
    ClerkUserListDTO,
    RoleUpdateResponseDTO,
    UserMetadataDTO
)
from users.models.dto.service_dto import UserTransformDTO, UserSearchResultDTO, UserMetadataServiceDTO, ServiceResponseDTO
from users.models.enums.user_role import UserRole

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserTransformDTO]:
        """Get user details by user ID from authentication service"""
        user_data = await self.auth_service.get_user_by_id(user_id)
        if user_data:
            return self._transform_user_data(user_data.dict())
        
        logger.warning(f"User {user_id} not found in Clerk, returning None")
        return None
    
    async def get_all_users(self) -> UserSearchResultDTO:
        """Get all users from authentication service"""
        users_response = await self.auth_service.get_all_users()
        transformed_users = [self._transform_user_data(user.dict()) for user in users_response.users]
        return UserSearchResultDTO(users=transformed_users, total_count=len(transformed_users))
    
    def _transform_user_data(self, user_data: Dict[str, Any]) -> UserTransformDTO:
        """Transform user data to match React app expectations"""
        return UserTransformDTO(
            user_id=user_data.get("id"),
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            role=user_data.get("public_metadata", {}).get("role", UserRole.USER.value),
            created_at=user_data.get("created_at"),
            updated_at=user_data.get("updated_at")
        )
    
    async def update_user_role(self, user_id: str, role: str) -> Optional[UserTransformDTO]:
        """Update user role via authentication service"""
        updated_user = await self.auth_service.update_user_role(user_id, role)
        if updated_user:
            return self._transform_user_data(updated_user.dict())
        return None
    

    
    async def search_users(self, query: str) -> List[Dict[str, Any]]:
        """Search users by email or name"""
        try:
            users_response = await self.auth_service.get_all_users()
            filtered_users = []
            
            for user in users_response.users:
                email = user.email or ""
                first_name = user.first_name or ""
                last_name = user.last_name or ""
                
                if (query.lower() in email.lower() or 
                    query.lower() in first_name.lower() or 
                    query.lower() in last_name.lower()):
                    filtered_users.append(self._transform_user_data(user.dict()))
            
            return filtered_users
        except Exception:
            return []
    
    async def get_user_metadata(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user metadata from authentication service"""
        try:
            user = await self.auth_service.get_user_by_id(user_id)
            if user:
                return {
                    "public_metadata": user.public_metadata,
                    "private_metadata": user.private_metadata
                }
            return None
        except Exception:
            return None 