from exceptions.base_exception import BaseException

class AuthenticationException(BaseException):
    def __init__(self):
        super().__init__(
            message="Authentication failed",
            code="authentication_error",
            status_code=401
        )

class AuthorizationException(BaseException):
    def __init__(self):
        super().__init__(
            message="Access denied",
            code="authorization_error",
            status_code=403
        )

class TokenExpiredException(BaseException):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            code="token_expired",
            status_code=401
        )

class InvalidTokenException(BaseException):
    def __init__(self):
        super().__init__(
            message="Invalid token provided",
            code="invalid_token",
            status_code=401
        )

class ClerkAPIException(BaseException):
    def __init__(self, message: str = "Clerk API error"):
        super().__init__(
            message=message,
            code="clerk_api_error",
            status_code=500
        ) 