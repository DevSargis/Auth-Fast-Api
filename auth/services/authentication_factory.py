from configs.auth_config import AUTH_PROVIDER
from auth.services.authentication_service import AuthenticationService
from auth.services.clerk_authentication_service import ClerkAuthenticationService
from auth.exceptions.authentication_exceptions import AuthenticationException

class AuthenticationFactory:
    @staticmethod
    def create_authentication_service() -> AuthenticationService:
        """Create authentication service based on AUTH_PROVIDER environment variable"""
        
        if AUTH_PROVIDER == "clerk":
            return ClerkAuthenticationService()
        else:
            raise AuthenticationException()
    
    @staticmethod
    def get_current_provider() -> str:
        """Get current authentication provider"""
        return AUTH_PROVIDER
    
 