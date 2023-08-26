from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self, status_code: int = None, detail: str = None):
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class TokenNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token not found"


class TokenNotValidException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is not valid"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class UserNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class InvalidEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password"


class NoRoomAvailableException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "No room available"
