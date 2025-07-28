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
    def __init__(self):
        self.clerk = None
        self._user_cache = {}
        self.base_url = CLERK_API_URL
        self.secret_key = CLERK_SECRET_KEY
    
    async def authenticate_user(self, request: Request) -> AuthenticationResponseDTO:
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
        """Convert timestamp to ISO format string"""
        if timestamp is None:
            return "2023-01-01T00:00:00Z"
        
        if isinstance(timestamp, int):
            dt = datetime.fromtimestamp(timestamp / 1000)
        elif isinstance(timestamp, str):
            return timestamp
        else:
            return "2023-01-01T00:00:00Z"
        
        return dt.isoformat() + "Z"
    
    async def _fetch_user_from_clerk(self, user_id: str) -> None:
        """Fetch user data from Clerk API"""
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
                        clerk_user = ClerkUserDTO(
                            id=user_data.get("id"),
                            email=user_data.get("email_addresses", [{}])[0].get("email_address") if user_data.get("email_addresses") else None,
                            first_name=user_data.get("first_name"),
                            last_name=user_data.get("last_name"),
                            public_metadata=user_data.get("public_metadata", {}),
                            private_metadata=user_data.get("private_metadata", {}),
                            created_at=self._convert_timestamp(user_data.get("created_at")),
                            updated_at=self._convert_timestamp(user_data.get("updated_at"))
                        )
                        self._user_cache[user_id] = clerk_user.dict()
                    else:
                        logger.error(f"Failed to fetch user {user_id} from Clerk: {response.status}")
        except Exception as e:
            logger.error(f"Error fetching user {user_id} from Clerk API: {str(e)}")
    
    async def get_user_by_id(self, user_id: str) -> Optional[ClerkUserDTO]:
        try:
            if user_id not in self._user_cache:
                await self._fetch_user_from_clerk(user_id)
            
            if user_id in self._user_cache:
                return ClerkUserDTO(**self._user_cache[user_id])
            
            return None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {str(e)}")
            return None
    
    async def get_all_users(self) -> ClerkUserListDTO:
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