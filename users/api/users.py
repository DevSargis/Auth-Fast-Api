from fastapi import APIRouter, Depends, Request
from auth.dependencies import get_authenticated_user
from users.dependencies import get_user_service
from users.services.user_service import UserService
from users.models.dto.user_dto import UserInfoDTO, UserMetadataResponse
from users.exceptions.user_exceptions import UserNotFoundException
import jwt

router = APIRouter(prefix="/users", tags=["users"])




@router.get("/me", response_model=UserInfoDTO)
async def get_my_profile(
    authenticated_user = Depends(get_authenticated_user),
    user_service: UserService = Depends(get_user_service)
):
    user_id = authenticated_user.get("sub")
    user_data = await user_service.get_user_by_id(user_id)
    
    if not user_data:
        raise UserNotFoundException(user_id)
    
    return UserInfoDTO(
        user_id=user_data.user_id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at
    )

@router.get("/me/metadata", response_model=UserMetadataResponse)
async def get_my_metadata(
    authenticated_user = Depends(get_authenticated_user),
    user_service: UserService = Depends(get_user_service)
):
    user_id = authenticated_user.get("sub")
    metadata = await user_service.get_user_metadata(user_id)
    
    if not metadata:
        raise UserNotFoundException(user_id)
    
    return UserMetadataResponse(
        public_metadata=metadata["public_metadata"],
        private_metadata=metadata["private_metadata"]
    )
