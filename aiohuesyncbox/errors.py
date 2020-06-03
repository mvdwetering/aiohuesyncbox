"""Aiohuesyncbox errors."""


class AiohuesyncboxException(Exception):
    """Base error for aiohuesyncbox."""


class RequestError(AiohuesyncboxException):
    """Unable to fulfill request.

    Raised when host or API cannot be reached.
    """

class Unauthorized(AiohuesyncboxException):
    """Application is not authorized."""


class InvalidState(AiohuesyncboxException):
    """Raised when the box is not in the correct state to handle the request."""


ERRORS = {
    1: Unauthorized,
    2: Unauthorized,
    3: Unauthorized,
    10: RequestError,
    11: RequestError,
    12: RequestError,
    13: RequestError,
    14: RequestError,
    15: RequestError,
    16: InvalidState,
}


def raise_error(code, message):
    cls = ERRORS.get(code, AiohuesyncboxException)
    raise cls("{}: {}".format(code, message))