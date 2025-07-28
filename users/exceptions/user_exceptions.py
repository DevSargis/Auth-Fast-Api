from exceptions.base_exception import BaseException

class UserNotFoundException(BaseException):
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User not found: {user_id}",
            code="user_not_found",
            status_code=404
        )

class UserAlreadyExistsException(BaseException):
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User already exists: {user_id}",
            code="user_already_exists",
            status_code=409
        )

class RoleUpdateForbiddenException(BaseException):
    def __init__(self):
        super().__init__(
            message="Role update forbidden",
            code="role_update_forbidden",
            status_code=403
        )

class UserValidationException(BaseException):
    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"User validation error: {field} - {message}",
            code="user_validation_error",
            status_code=400
        )

class UserServiceException(BaseException):
    def __init__(self, message: str = "User service error"):
        super().__init__(
            message=message,
            code="user_service_error",
            status_code=500
        ) 