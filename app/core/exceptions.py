class AppError(Exception):
    def __init__(self, message: str = "An unexpected error occurred"):
        self.message = message
        super().__init__(message)

class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required: missing or invalid token"):
        super().__init__(message)

class AuthorizationError(AppError):
    pass

class NotFoundError(AppError):
    pass
