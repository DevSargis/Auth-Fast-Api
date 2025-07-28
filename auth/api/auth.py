"""
Authentication API Endpoints

This module provides authentication-related API endpoints for user authentication and profile management.

Endpoints:
- GET /auth/me: Get current authenticated user information
  - Returns user ID, email, and role from JWT token
  - Requires valid Bearer token in Authorization header
  - Uses Clerk authentication service for token validation

Dependencies:
- get_authenticated_user: FastAPI dependency for user authentication
- CurrentUserResponseDTO: Response model for user data

Security:
- All endpoints require valid JWT token
- Token validation handled by Clerk authentication service
- Role information extracted from user metadata

Example Usage:
    GET /api/v1/auth/me
    Authorization: Bearer <jwt_token>
    
    Response:
    {
        "user_id": "user_123",
        "email": "user@example.com",
        "role": "USER"
    }
"""

from fastapi import APIRouter, Depends
from auth.dependencies import get_authenticated_user
from auth.models.dto.api_dto import CurrentUserResponseDTO
from users.models.enums.user_role import UserRole

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me", response_model=CurrentUserResponseDTO)
async def get_current_user(
    authenticated_user = Depends(get_authenticated_user)
):
    """
    Get current authenticated user information.
    
    Extracts user details from JWT token and returns user profile.
    Role is retrieved from user's public metadata in Clerk.
    
    Args:
        authenticated_user: User data from JWT token (injected by dependency)
        
    Returns:
        CurrentUserResponseDTO: User ID, email, and role
        
    Raises:
        AuthenticationException: If token is invalid or missing
    """
    return CurrentUserResponseDTO(
        user_id=authenticated_user.get("sub"),
        email=authenticated_user.get("email"),
        role=authenticated_user.get("public_metadata", {}).get("role", UserRole.USER.value)
    ) 