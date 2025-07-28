from fastapi import Depends
from auth.dependencies import get_authentication_service
from auth.services.authentication_service import AuthenticationService
from users.services.user_service import UserService

def get_user_service(
    auth_service: AuthenticationService = Depends(get_authentication_service)
) -> UserService:
    return UserService(auth_service)
