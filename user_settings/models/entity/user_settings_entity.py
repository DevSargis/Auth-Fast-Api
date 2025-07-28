from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserSettings:
    id: Optional[int]
    user_id: str
    address: str
    street: str
    passport_code: str
    language: str
    timezone: str
    push_notifications: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: str,
        address: str = "",
        street: str = "",
        passport_code: str = "",
        language: str = "en",
        timezone: str = "UTC",
        push_notifications: bool = True
    ) -> "UserSettings":
        now = datetime.utcnow()
        return cls(
            id=None,
            user_id=user_id,
            address=address,
            street=street,
            passport_code=passport_code,
            language=language,
            timezone=timezone,
            push_notifications=push_notifications,
            created_at=now,
            updated_at=now
        )

    def update(
        self,
        address: Optional[str] = None,
        street: Optional[str] = None,
        passport_code: Optional[str] = None,
        language: Optional[str] = None,
        timezone: Optional[str] = None,
        push_notifications: Optional[bool] = None
    ) -> None:
        if address is not None:
            self.address = address
        if street is not None:
            self.street = street
        if passport_code is not None:
            self.passport_code = passport_code
        if language is not None:
            self.language = language
        if timezone is not None:
            self.timezone = timezone
        if push_notifications is not None:
            self.push_notifications = push_notifications
        self.updated_at = datetime.utcnow() 