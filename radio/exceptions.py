from rest_framework.exceptions import APIException


class InvalidBackend(APIException):
    """Simple exception used to show that an invalid backend has been used"""
    status_code = 404
    default_detail = 'Invalid backend, provider not recognised.'


class MissingParameter(APIException):
    """Simple exception used to show missing params on the search endpoint"""
    status_code = 400
    default_detail = 'Required parameters are missing.'


class OauthFailed(APIException):
    """Simple exception used to show user auth failed"""
    status_code = 403
    default_detail = 'Failed to authenticate user from source type.'


class ThridPartyOauthRequired(APIException):
    """Simple exception used to show thrid party oauth required"""
    status_code = 403
    default_detail = 'Thrid party authentication failed.'


class RecordDeleteFailed(APIException):
    """Simple exception used to show record could not be removed from database
    """
    status_code = 400
    default_detail = 'The record could not be removed from the database.'


class RecordNotFound(APIException):
    """Simple exception used to show record was not found in database"""
    status_code = 404
    default_detail = 'The record could not be found.'


class RecordNotSaved(APIException):
    """Simple exception used to show record could not be saved to database"""
    status_code = 400
    default_detail = 'The record could not be saved.'


class QueueEmpty(APIException):
    """Simple exception used to show queue has no records (historic or active).
    """
    status_code = 400
    default_detail = 'This queue has no tracks.'
