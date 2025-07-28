from fastapi import APIRouter, Depends
from user_settings.dependencies import get_user_settings_service
from user_settings.services.user_settings_service import UserSettingsService
from user_settings.models.dto.user_settings_dto import UserSettingsDTO, UserSettingsUpdateDTO
from auth.dependencies import get_authenticated_user

router = APIRouter(prefix="/user-settings", tags=["user-settings"])

@router.get("/me", response_model=UserSettingsDTO)
async def get_my_settings(
    authenticated_user = Depends(get_authenticated_user),
    service: UserSettingsService = Depends(get_user_settings_service)
):
    user_id = authenticated_user.get("sub")
    user_settings = await service.get_user_settings(user_id)
    
    if not user_settings:
        default_settings = UserSettingsUpdateDTO()
        user_settings = await service.create_user_settings(user_id, default_settings)
    
    return user_settings

@router.put("/me", response_model=UserSettingsDTO)
async def update_my_settings(
    settings_data: UserSettingsUpdateDTO,
    authenticated_user = Depends(get_authenticated_user),
    service: UserSettingsService = Depends(get_user_settings_service)
):
    user_id = authenticated_user.get("sub")
    updated_settings = await service.update_user_settings(user_id, settings_data)
    
    if not updated_settings:
        updated_settings = await service.create_user_settings(user_id, settings_data)
    
    return updated_settings 