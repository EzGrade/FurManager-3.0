from src.utils.enums.exception import ExceptionCodes
from src.utils.exceptions.base import BaseApplicationException


class NoRecordsFoundException(BaseApplicationException):
    status_code = 404

    application_error_code = ExceptionCodes.DATABASE_ERROR
    title = "No Records Found"


class InvalidValueException(BaseApplicationException):
    status_code = 400

    application_error_code = ExceptionCodes.VALIDATION_ERROR


class ConflictError(BaseApplicationException):
    status_code = 409

    application_error_code = ExceptionCodes.DATABASE_ERROR
