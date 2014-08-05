from rest_framework.exceptions import APIException


class NotAuthorised(APIException):
    """
    Simple exception used to show that the request requires auth
    """
    status_code = 401
    default_detail = 'Not authorised'


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
    default_detail = 'Required parameters are missing'
