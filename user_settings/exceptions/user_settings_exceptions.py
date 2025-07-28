from exceptions.base_exception import BaseException

class UserSettingsNotFoundException(BaseException):
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User settings not found for user: {user_id}",
            code="user_settings_not_found",
            status_code=404
        )

class UserSettingsAlreadyExistsException(BaseException):
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User settings already exist for user: {user_id}",
            code="user_settings_already_exists",
            status_code=409
        )

class UserSettingsValidationException(BaseException):
    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"User settings validation error: {field} - {message}",
            code="user_settings_validation_error",
            status_code=400
        )

class UserSettingsServiceException(BaseException):
    def __init__(self, message: str = "User settings service error"):
        super().__init__(
            message=message,
            code="user_settings_service_error",
            status_code=500
        )

class UserSettingsRepositoryException(BaseException):
    def __init__(self, message: str = "User settings repository error"):
        super().__init__(
            message=message,
            code="user_settings_repository_error",
            status_code=500
        ) 