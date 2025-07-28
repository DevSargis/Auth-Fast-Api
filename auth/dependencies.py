import logging
from fastapi import Depends, Request
from auth.services.authentication_factory import AuthenticationFactory
from auth.services.authentication_service import AuthenticationService
from users.models.enums.user_role import UserRole
from auth.exceptions.authentication_exceptions import AuthenticationException, AuthorizationException

logger = logging.getLogger(__name__)

def get_authentication_service() -> AuthenticationService:
    return AuthenticationFactory.create_authentication_service()

async def get_authenticated_user(
    request: Request,
    auth_service: AuthenticationService = Depends(get_authentication_service)
):
    try:
        auth_response = await auth_service.authenticate_user(request)
        return auth_response.dict()
    except Exception as e:
        raise AuthenticationException()

async def require_admin_user(
    authenticated_user = Depends(get_authenticated_user)
):
    if not authenticated_user:
        raise AuthenticationException()
        
    role = authenticated_user.get("public_metadata", {}).get("role", UserRole.USER.value)
    
    if role != UserRole.ADMIN.value:
        logger.warning(f"Admin check - Access denied. User role: {role}")
        raise AuthorizationException()
    
    logger.info(f"Admin check - Access granted for user: {authenticated_user.get('sub')}")
    return authenticated_user
