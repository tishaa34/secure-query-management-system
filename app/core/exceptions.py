class DomainError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=404)


class AuthorizationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=403)


class AuthenticationError(DomainError):
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message=message, status_code=401)


class ValidationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)
