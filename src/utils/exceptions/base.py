from src.utils.enums.exception import ExceptionCodes


class BaseApplicationException(Exception):
    status_code = 500

    application_error_code: str = ExceptionCodes.DEFAULT_CODE

    def __init__(self, message: str, details: dict | None = None):
        self.message: str = message
        self.details = details


class BaseRepositoryException(Exception):
    pass
