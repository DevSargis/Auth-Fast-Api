from exceptions.base_exception import BaseException

class DatabaseConnectionException(BaseException):
    def __init__(self):
        super().__init__(
            message="Database connection failed",
            code="database_connection_error",
            status_code=500
        ) 