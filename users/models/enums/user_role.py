from enum import Enum
from typing import Dict, Any

class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    
    @classmethod
    def from_string(cls, role_string: str) -> "UserRole":
        """Convert string to UserRole enum"""
        try:
            return cls(role_string.upper())
        except ValueError:
            return cls.USER  # Default to USER if invalid
    
    @classmethod
    def from_user_metadata(cls, metadata: Dict[str, Any]) -> "UserRole":
        """Extract role from user metadata safely"""
        role_string = metadata.get("role", cls.USER.value)
        return cls.from_string(role_string)
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"UserRole.{self.name}" 