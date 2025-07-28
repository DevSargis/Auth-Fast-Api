"""
User Settings Repository

This module provides data access layer for user settings using the Repository pattern.
It abstracts database operations and provides a clean interface for user settings CRUD operations.

Repository Pattern Implementation:
- Abstract base class defining the interface
- SQLAlchemy implementation for PostgreSQL
- Clean separation between business logic and data access
- Type-safe operations with proper error handling

Key Features:
- User settings CRUD operations
- Database abstraction layer
- SQLAlchemy integration
- Transaction management
- Error handling and logging

Database Schema:
- user_settings table with user_id, address, street, passport_code, etc.
- Timestamps for created_at and updated_at
- Foreign key relationship with users table

Dependencies:
- SQLAlchemy: Database ORM
- AsyncSession: For async database operations
- UserSettings: Entity model
- UserSettingsModel: Database model

Error Handling:
- ValueError: For user settings not found
- DatabaseConnectionException: For database connection issues
- RepositoryException: For general repository errors

Example Usage:
    repository = SQLAlchemyUserSettingsRepository(session)
    settings = await repository.get_by_user_id("user_123")
    new_settings = await repository.create(user_settings)
    updated_settings = await repository.update(user_settings)
"""

from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from user_settings.models.entity.user_settings_entity import UserSettings
from user_settings.models.schema.user_settings_model import UserSettingsModel

class UserSettingsRepository(ABC):
    """
    Abstract base class for user settings repository.
    
    Defines the interface for user settings data access operations.
    Implementations should provide concrete database operations.
    
    Methods:
        get_by_user_id: Retrieve user settings by user ID
        create: Create new user settings
        update: Update existing user settings
    """
    
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[UserSettings]:
        """
        Get user settings by user ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            Optional[UserSettings]: User settings or None if not found
        """
        pass
    
    @abstractmethod
    async def create(self, user_settings: UserSettings) -> UserSettings:
        """
        Create new user settings.
        
        Args:
            user_settings: UserSettings entity to create
            
        Returns:
            UserSettings: Created user settings with ID
        """
        pass
    
    @abstractmethod
    async def update(self, user_settings: UserSettings) -> UserSettings:
        """
        Update existing user settings.
        
        Args:
            user_settings: UserSettings entity to update
            
        Returns:
            UserSettings: Updated user settings
            
        Raises:
            ValueError: If user settings not found
        """
        pass

class SQLAlchemyUserSettingsRepository(UserSettingsRepository):
    """
    SQLAlchemy implementation of user settings repository.
    
    Provides concrete implementation using SQLAlchemy ORM for PostgreSQL.
    Handles database operations with proper transaction management.
    
    Attributes:
        session: SQLAlchemy async session for database operations
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def get_by_user_id(self, user_id: str) -> Optional[UserSettings]:
        """
        Get user settings by user ID from database.
        
        Queries the user_settings table for the given user ID.
        Transforms database model to entity model.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            Optional[UserSettings]: User settings entity or None if not found
        """
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
        """
        Create new user settings in database.
        
        Creates a new record in the user_settings table.
        Commits transaction and refreshes the model.
        
        Args:
            user_settings: UserSettings entity to create
            
        Returns:
            UserSettings: Created user settings with database ID
        """
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
        """
        Update existing user settings in database.
        
        Finds existing record by user_id and updates all fields.
        Commits transaction and refreshes the model.
        
        Args:
            user_settings: UserSettings entity to update
            
        Returns:
            UserSettings: Updated user settings
            
        Raises:
            ValueError: If user settings not found
        """
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