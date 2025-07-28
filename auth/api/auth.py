from fastapi import APIRouter, Depends
from auth.dependencies import get_authenticated_user
from auth.models.dto.api_dto import CurrentUserResponseDTO
from users.models.enums.user_role import UserRole

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me", response_model=CurrentUserResponseDTO)
async def get_current_user(
    authenticated_user = Depends(get_authenticated_user)
):
    return CurrentUserResponseDTO(
        user_id=authenticated_user.get("sub"),
        email=authenticated_user.get("email"),
        role=authenticated_user.get("public_metadata", {}).get("role", UserRole.USER.value)
    ) 