from rest_framework.exceptions import APIException


class InvalidBackend(APIException):
    """
    Simple exception used to show that an invalid backend has been used
    """
    status_code = 404
    default_detail = 'Invalid backend, provider not recognised.'


class InvalidLookupType(APIException):
    """
    Simple exception used to show that an invalid source has been used
    """
    status_code = 404
    default_detail = 'Invalid lookup_type, type not supported by backend.'


class MissingParameter(APIException):
    """
    Simple exception used to show missing params on the search endpoint
    """
    status_code = 400
    default_detail = 'Required parameters are missing.'


class RecordDeleteFailed(APIException):
    """
    Simple exception used to show record could not be removed from database
    """
    status_code = 400
    default_detail = 'The record could not be removed from the database.'


class RecordNotFound(APIException):
    """
    Simple exception used to show record was not found in database
    """
    status_code = 404
    default_detail = 'The record could not be found.'


class RecordNotSaved(APIException):
    """
    Simple exception used to show record could not be saved to database
    """
    status_code = 400
    default_detail = 'The record could not be saved.'
