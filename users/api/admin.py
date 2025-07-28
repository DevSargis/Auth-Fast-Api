"""
Admin API Endpoints

This module provides administrative endpoints for user management and role administration.
All endpoints require ADMIN role authentication.

Endpoints:
- GET /admin/users: Get all users (admin only)
  - Returns list of all users with pagination
  - Uses UserService for data retrieval
  - Requires ADMIN role authentication

- POST /admin/users/{user_id}/set-role: Set user role (admin only)
  - Updates user role via query parameter
  - Requires ADMIN role authentication
  - Uses UserService for role updates

- PUT /admin/users/{user_id}/role: Update user role (admin only)
  - Updates user role via request body
  - Requires ADMIN role authentication
  - Uses UserService for role updates

- GET /admin/users/search: Search users (admin only)
  - Search users by email or name
  - Requires ADMIN role authentication
  - Uses UserService for search functionality

- POST /admin/set-admin: Set current user as admin (admin only)
  - Promotes current user to ADMIN role
  - Requires ADMIN role authentication
  - Uses UserService for role updates

Dependencies:
- require_admin_user: FastAPI dependency for admin authentication
- get_user_service: FastAPI dependency for UserService injection
- UserService: Business logic for user operations

Security:
- All endpoints require ADMIN role
- Role-based access control enforced
- User operations logged for audit

Example Usage:
    GET /api/v1/admin/users
    Authorization: Bearer <admin_jwt_token>
    
    Response:
    {
        "users": [...],
        "total_count": 10
    }
"""

import os
from fastapi import APIRouter, Depends, Query, Request
from dotenv import load_dotenv
from auth.dependencies import require_admin_user
from users.dependencies import get_user_service
from users.services.user_service import UserService
from users.models.dto.user_dto import RoleUpdateResponse, RoleUpdateRequest
from users.exceptions.user_exceptions import RoleUpdateForbiddenException
from users.exceptions.user_exceptions import UserServiceException
from auth.models.dto.api_dto import AdminRoleUpdateResponseDTO
from users.models.dto.service_dto import UserSearchResultDTO
from users.models.enums.user_role import UserRole

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=UserSearchResultDTO)
async def get_all_users(
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get all users (admin only).
    
    Retrieves list of all users from authentication service.
    Requires ADMIN role authentication.
    
    Args:
        admin_user: Authenticated admin user (injected by dependency)
        user_service: User service for business logic (injected by dependency)
        
    Returns:
        UserSearchResultDTO: List of users with total count
        
    Raises:
        UserServiceException: If user retrieval fails
        AuthorizationException: If user is not admin
    """
    try:
        users_result = await user_service.get_all_users()
        return users_result
    except Exception as e:
        raise UserServiceException("Failed to retrieve users")

@router.post("/users/{user_id}/set-role", response_model=RoleUpdateResponse)
async def set_user_role(
    user_id: str,
    role: str = Query(..., description="New role for the user"),
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Set user role via query parameter (admin only).
    
    Updates user role using query parameter.
    Requires ADMIN role authentication.
    
    Args:
        user_id: ID of user to update
        role: New role for the user
        admin_user: Authenticated admin user (injected by dependency)
        user_service: User service for business logic (injected by dependency)
        
    Returns:
        RoleUpdateResponse: Confirmation of role update
        
    Raises:
        RoleUpdateForbiddenException: If role update fails
        AuthorizationException: If user is not admin
    """
    try:
        updated_user = await user_service.update_user_role(user_id, role)
        return RoleUpdateResponse(
            user_id=user_id,
            role=role,
            success=True
        )
    except Exception as e:
        raise RoleUpdateForbiddenException()

@router.put("/users/{user_id}/role", response_model=RoleUpdateResponse)
async def update_user_role(
    user_id: str,
    role_data: RoleUpdateRequest,
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update user role via request body (admin only).
    
    Updates user role using request body data.
    Requires ADMIN role authentication.
    
    Args:
        user_id: ID of user to update
        role_data: Role update request data
        admin_user: Authenticated admin user (injected by dependency)
        user_service: User service for business logic (injected by dependency)
        
    Returns:
        RoleUpdateResponse: Confirmation of role update
        
    Raises:
        RoleUpdateForbiddenException: If role update fails
        AuthorizationException: If user is not admin
    """
    try:
        updated_user = await user_service.update_user_role(user_id, role_data.role)
        return RoleUpdateResponse(
            user_id=user_id,
            role=role_data.role,
            success=True
        )
    except Exception as e:
        raise RoleUpdateForbiddenException()

@router.get("/users/search", response_model=UserSearchResultDTO)
async def search_users(
    query: str,
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Search users by email or name (admin only).
    
    Searches users by email, first name, or last name.
    Requires ADMIN role authentication.
    
    Args:
        query: Search query string
        admin_user: Authenticated admin user (injected by dependency)
        user_service: User service for business logic (injected by dependency)
        
    Returns:
        UserSearchResultDTO: Filtered list of users
        
    Raises:
        UserServiceException: If search fails
        AuthorizationException: If user is not admin
    """
    try:
        users = await user_service.search_users(query)
        return UserSearchResultDTO(users=users, total_count=len(users))
    except Exception as e:
        raise UserServiceException("Failed to search users")

@router.post("/set-admin", response_model=AdminRoleUpdateResponseDTO)
async def set_user_as_admin(
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Set current user as admin (admin only).
    
    Promotes the current authenticated user to ADMIN role.
    Requires ADMIN role authentication.
    
    Args:
        admin_user: Authenticated admin user (injected by dependency)
        user_service: User service for business logic (injected by dependency)
        
    Returns:
        AdminRoleUpdateResponseDTO: Confirmation of admin promotion
        
    Raises:
        RoleUpdateForbiddenException: If role update fails
        AuthorizationException: If user is not admin
    """
    user_id = admin_user.get("sub")
    try:
        updated_user = await user_service.update_user_role(user_id, UserRole.ADMIN.value)
        return AdminRoleUpdateResponseDTO(
            message="User role updated to ADMIN",
            user_id=user_id,
            updated_user=updated_user
        )
    except Exception as e:
        raise RoleUpdateForbiddenException() 