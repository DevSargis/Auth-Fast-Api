"""
Clerk Authentication Service

This module implements the Clerk authentication service, providing JWT token validation,
user management, and role-based access control integration with Clerk's API.

Key Features:
- JWT token validation and decoding
- User data retrieval from Clerk API
- Role management and updates
- User metadata handling
- Token expiration checking

Authentication Flow:
1. Extract Bearer token from Authorization header
2. Decode JWT token (without signature verification for Clerk)
3. Extract user information from token payload
4. Fetch additional user data from Clerk API if needed
5. Return authenticated user data

Dependencies:
- aiohttp: For async HTTP requests to Clerk API
- jwt: For JWT token decoding
- AuthenticationService: Abstract base class

Configuration:
- CLERK_SECRET_KEY: Clerk secret key for API access
- CLERK_API_URL: Clerk API base URL

Error Handling:
- InvalidTokenException: For malformed or invalid tokens
- TokenExpiredException: For expired tokens
- ClerkAPIException: For Clerk API communication errors

Example Usage:
    service = ClerkAuthenticationService()
    user_data = await service.authenticate_user(request)
    all_users = await service.get_all_users()
    updated_user = await service.update_user_role(user_id, "ADMIN")
"""

import jwt
import aiohttp
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import Request
from auth.services.authentication_service import AuthenticationService
from configs.auth_config import CLERK_SECRET_KEY, CLERK_API_URL
from auth.models.dto.authentication_dto import (
    AuthenticationResponseDTO,
    ClerkUserDTO,
    ClerkUserListDTO,
    TokenValidationDTO,
    UserMetadataDTO,
    RoleUpdateResponseDTO,
)
from auth.exceptions.authentication_exceptions import InvalidTokenException, TokenExpiredException, ClerkAPIException

logger = logging.getLogger(__name__)

class ClerkAuthenticationService(AuthenticationService):
    """
    Clerk Authentication Service Implementation.
    
    Provides authentication functionality using Clerk's JWT tokens and API.
    Handles user authentication, role management, and user data retrieval.
    
    Attributes:
        clerk: Clerk client instance (not used in current implementation)
        _user_cache: In-memory cache for user data
        base_url: Clerk API base URL
        secret_key: Clerk secret key for API access
    """
    
    def __init__(self):
        """
        Initialize Clerk authentication service.
        
        Sets up API configuration and user cache.
        """
        self.clerk = None
        self._user_cache = {}
        self.base_url = CLERK_API_URL
        self.secret_key = CLERK_SECRET_KEY
    
    async def authenticate_user(self, request: Request) -> AuthenticationResponseDTO:
        """
        Authenticate user from request headers.
        
        Extracts and validates JWT token from Authorization header.
        Fetches additional user data from Clerk if needed.
        
        Args:
            request: FastAPI request object containing Authorization header
            
        Returns:
            AuthenticationResponseDTO: Authenticated user data
            
        Raises:
            InvalidTokenException: If token is missing or invalid
            TokenExpiredException: If token has expired
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise InvalidTokenException()
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get("sub")
            
            if user_id:
                await self._fetch_user_from_clerk(user_id)
                user_data = self._user_cache.get(user_id, {})
                public_metadata = user_data.get("public_metadata", {})
            else:
                public_metadata = {}
            
            return AuthenticationResponseDTO(
                sub=payload.get("sub"),
                email=payload.get("email"),
                public_metadata=public_metadata
            )
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
    
    def _convert_timestamp(self, timestamp) -> str:
        """
        Convert timestamp to ISO format string.
        
        Args:
            timestamp: Unix timestamp or datetime object
            
        Returns:
            str: ISO formatted datetime string
        """
        if timestamp:
            if isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp).isoformat()
            elif isinstance(timestamp, str):
                return timestamp
        return None
    
    async def _fetch_user_from_clerk(self, user_id: str) -> None:
        """
        Fetch user data from Clerk API.
        
        Retrieves user information from Clerk and caches it.
        
        Args:
            user_id: Clerk user ID
        """
        if user_id in self._user_cache:
            return
        
        try:
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/users/{user_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        self._user_cache[user_id] = user_data
                    else:
                        logger.error(f"Failed to fetch user {user_id} from Clerk: {response.status}")
        except Exception as e:
            logger.error(f"Error fetching user {user_id} from Clerk: {str(e)}")
    
    async def get_user_by_id(self, user_id: str) -> Optional[ClerkUserDTO]:
        """
        Get user details by user ID.
        
        Fetches user data from Clerk API and transforms it to DTO.
        
        Args:
            user_id: Clerk user ID
            
        Returns:
            Optional[ClerkUserDTO]: User data or None if not found
        """
        try:
            await self._fetch_user_from_clerk(user_id)
            user_data = self._user_cache.get(user_id)
            
            if user_data:
                return ClerkUserDTO(
                    id=user_data.get("id"),
                    email=user_data.get("email_addresses", [{}])[0].get("email_address") if user_data.get("email_addresses") else None,
                    first_name=user_data.get("first_name"),
                    last_name=user_data.get("last_name"),
                    public_metadata=user_data.get("public_metadata", {}),
                    private_metadata=user_data.get("private_metadata", {}),
                    created_at=self._convert_timestamp(user_data.get("created_at")),
                    updated_at=self._convert_timestamp(user_data.get("updated_at"))
                )
            return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {str(e)}")
            return None
    
    async def get_all_users(self) -> ClerkUserListDTO:
        """
        Get all users from Clerk API.
        
        Fetches all users from Clerk and transforms them to DTOs.
        
        Returns:
            ClerkUserListDTO: List of all users with total count
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/users",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        users_data = await response.json()
                        users = []
                        for user_data in users_data:
                            user = ClerkUserDTO(
                                id=user_data.get("id"),
                                email=user_data.get("email_addresses", [{}])[0].get("email_address") if user_data.get("email_addresses") else None,
                                first_name=user_data.get("first_name"),
                                last_name=user_data.get("last_name"),
                                public_metadata=user_data.get("public_metadata", {}),
                                private_metadata=user_data.get("private_metadata", {}),
                                created_at=self._convert_timestamp(user_data.get("created_at")),
                                updated_at=self._convert_timestamp(user_data.get("updated_at"))
                            )
                            users.append(user)
                            self._user_cache[user_data.get("id")] = user.dict()
                        return ClerkUserListDTO(users=users, total_count=len(users))
                    else:
                        logger.error(f"Failed to fetch users from Clerk: {response.status}")
                        return ClerkUserListDTO(users=[], total_count=0)
        except Exception as e:
            logger.error(f"Error fetching all users: {str(e)}")
            return ClerkUserListDTO(users=[], total_count=0)
    
    async def update_user_role(self, user_id: str, role: str) -> RoleUpdateResponseDTO:
        """
        Update user role via Clerk API.
        
        Updates user's public metadata with new role.
        
        Args:
            user_id: Clerk user ID
            role: New role for the user
            
        Returns:
            RoleUpdateResponseDTO: Confirmation of role update
            
        Raises:
            ClerkAPIException: If role update fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "public_metadata": {"role": role}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    f"{self.base_url}/users/{user_id}",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        if user_id in self._user_cache:
                            self._user_cache[user_id]["public_metadata"]["role"] = role
                        
                        return RoleUpdateResponseDTO(
                            id=user_id,
                            public_metadata={"role": role}
                        )
                    else:
                        raise ClerkAPIException(f"Failed to update user role: {response.status}")
        except Exception as e:
            raise ClerkAPIException(f"Failed to update user role: {str(e)}")
    
    async def is_token_expired(self, token: str) -> TokenValidationDTO:
        """
        Check if JWT token is expired.
        
        Decodes token and checks expiration without signature verification.
        
        Args:
            token: JWT token string
            
        Returns:
            TokenValidationDTO: Token validation result
            
        Raises:
            TokenExpiredException: If token has expired
            InvalidTokenException: If token is invalid
        """
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return TokenValidationDTO(
                is_expired=False,
                is_valid=True,
                payload=payload
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()
    
    
    async def get_user_metadata(self, user_id: str) -> Optional[UserMetadataDTO]:
        """
        Get user metadata from cache or Clerk API.
        
        Retrieves user's public and private metadata.
        
        Args:
            user_id: Clerk user ID
            
        Returns:
            Optional[UserMetadataDTO]: User metadata or None if not found
        """
        try:
            if user_id in self._user_cache:
                user = self._user_cache[user_id]
                return UserMetadataDTO(
                    public_metadata=user.get("public_metadata", {}),
                    private_metadata=user.get("private_metadata", {})
                )
            return None
        except Exception:
            return None 