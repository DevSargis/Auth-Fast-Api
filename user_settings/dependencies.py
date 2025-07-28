from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from configs.database_config import get_session
from user_settings.repository.user_settings_repository import SQLAlchemyUserSettingsRepository, UserSettingsRepository
from user_settings.services.user_settings_service import UserSettingsService

def get_user_settings_repository(session: AsyncSession = Depends(get_session)) -> UserSettingsRepository:
    return SQLAlchemyUserSettingsRepository(session)

def get_user_settings_service(
    repository: UserSettingsRepository = Depends(get_user_settings_repository)
) -> UserSettingsService:
    return UserSettingsService(repository)
