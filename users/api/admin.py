import os
from fastapi import APIRouter, Depends, Query, Request
from dotenv import load_dotenv
from auth.dependencies import require_admin_user
from users.dependencies import get_user_service
from users.services.user_service import UserService
from users.models.dto.user_dto import RoleUpdateResponse, RoleUpdateRequest
from users.models.dto.service_dto import UserSearchResultDTO
from users.exceptions.user_exceptions import RoleUpdateForbiddenException
from users.exceptions.user_exceptions import UserServiceException
from auth.models.dto.api_dto import AdminRoleUpdateResponseDTO
from users.models.enums.user_role import UserRole

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=UserSearchResultDTO)
async def get_all_users(
    admin_user=Depends(require_admin_user),
    user_service: UserService = Depends(get_user_service)
):
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
    """Set the current user as admin"""
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