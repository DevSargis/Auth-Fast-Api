from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from user_settings.models.entity.user_settings_entity import UserSettings
from user_settings.models.schema.user_settings_model import UserSettingsModel

class UserSettingsRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[UserSettings]:
        pass
    
    @abstractmethod
    async def create(self, user_settings: UserSettings) -> UserSettings:
        pass
    
    @abstractmethod
    async def update(self, user_settings: UserSettings) -> UserSettings:
        pass

class SQLAlchemyUserSettingsRepository(UserSettingsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str) -> Optional[UserSettings]:
        result = await self.session.execute(
            select(UserSettingsModel).where(UserSettingsModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return None
            
        return UserSettings(
            id=model.id,
            user_id=model.user_id,
            address=model.address,
            street=model.street,
            passport_code=model.passport_code,
            language=model.language,
            timezone=model.timezone,
            push_notifications=model.push_notifications,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def create(self, user_settings: UserSettings) -> UserSettings:
        model = UserSettingsModel(
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
        
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        
        user_settings.id = model.id
        return user_settings

    async def update(self, user_settings: UserSettings) -> UserSettings:
        result = await self.session.execute(
            select(UserSettingsModel).where(UserSettingsModel.user_id == user_settings.user_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError("User settings not found")
        
        model.address = user_settings.address
        model.street = user_settings.street
        model.passport_code = user_settings.passport_code
        model.language = user_settings.language
        model.timezone = user_settings.timezone
        model.push_notifications = user_settings.push_notifications
        model.updated_at = user_settings.updated_at
        
        await self.session.commit()
        await self.session.refresh(model)
        
        return user_settings 