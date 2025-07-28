from typing import Optional
from user_settings.models.entity.user_settings_entity import UserSettings
from user_settings.repository.user_settings_repository import UserSettingsRepository
from user_settings.models.dto.user_settings_dto import UserSettingsDTO, UserSettingsUpdateDTO

class UserSettingsService:
    def __init__(self, repository: UserSettingsRepository):
        self.repository = repository
    
    async def get_user_settings(self, user_id: str) -> Optional[UserSettingsDTO]:
        user_settings = await self.repository.get_by_user_id(user_id)
        if user_settings:
            return UserSettingsDTO(
                id=user_settings.id,
                user_id=user_settings.user_id,
                address=user_settings.address,
                street=user_settings.street,
                passport_code=user_settings.passport_code,
                language=user_settings.language,
                timezone=user_settings.timezone,
                push_notifications=user_settings.push_notifications,
                created_at=user_settings.created_at,
                updated_at=user_settings.updated_at
            )
        return None
    
    async def create_user_settings(self, user_id: str, settings_data: UserSettingsUpdateDTO) -> UserSettingsDTO:
        user_settings = UserSettings.create(
            user_id=user_id,
            address=settings_data.address or "",
            street=settings_data.street or "",
            passport_code=settings_data.passport_code or "",
            language=settings_data.language or "en",
            timezone=settings_data.timezone or "UTC",
            push_notifications=settings_data.push_notifications if settings_data.push_notifications is not None else True
        )
        
        created_settings = await self.repository.create(user_settings)
        
        return UserSettingsDTO(
            id=created_settings.id,
            user_id=created_settings.user_id,
            address=created_settings.address,
            street=created_settings.street,
            passport_code=created_settings.passport_code,
            language=created_settings.language,
            timezone=created_settings.timezone,
            push_notifications=created_settings.push_notifications,
            created_at=created_settings.created_at,
            updated_at=created_settings.updated_at
        )
    
    async def update_user_settings(self, user_id: str, settings_data: UserSettingsUpdateDTO) -> Optional[UserSettingsDTO]:
        existing_settings = await self.repository.get_by_user_id(user_id)
        if not existing_settings:
            return None
        
        existing_settings.update(
            address=settings_data.address,
            street=settings_data.street,
            passport_code=settings_data.passport_code,
            language=settings_data.language,
            timezone=settings_data.timezone,
            push_notifications=settings_data.push_notifications
        )
        
        updated_settings = await self.repository.update(existing_settings)
        
        return UserSettingsDTO(
            id=updated_settings.id,
            user_id=updated_settings.user_id,
            address=updated_settings.address,
            street=updated_settings.street,
            passport_code=updated_settings.passport_code,
            language=updated_settings.language,
            timezone=updated_settings.timezone,
            push_notifications=updated_settings.push_notifications,
            created_at=updated_settings.created_at,
            updated_at=updated_settings.updated_at
        ) 