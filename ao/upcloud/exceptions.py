from rest_framework import exceptions
from ao.core.views import exception_handler



class APIException(exceptions.APIException):
    def get_full_details(self):
        return {
            'error': {
                'error_code': self.detail.code,
                'error_message': self.detail
            }
        }

    def get_response(self):
        return exception_handler(self, None)


class ServerInvalid(APIException):
    status_code = 400
    default_detail = 'SERVER_INVALID' 
    default_code = 'The server UUID has an invalid value.'


class ServerDoesNotExist(APIException):
    status_code = 404
    default_detail = 'SERVER_NOT_FOUND' 
    default_code = 'The server does not exist.'


class ServerForbidden(APIException):
    status_code = 403
    default_detail = 'SERVER_FORBIDDEN' 
    default_code = 'The server exists, but is owned by another account.'


class ServerStateIllegal(APIException):
    status_code = 409
    default_detail = 'SERVER_STATE_ILLEGAL' 
    default_code = 'The server is in a state in which it cannot be used.'


class IpAddressNotFound(APIException):
    status_code = 404
    default_detail = 'IP_ADDRESS_NOT_FOUND' 
    default_code = 'The IP address does not exist.'


class IpAddressForbidden(APIException):
    status_code = 403
    default_detail = 'IP_ADDRESS_FORBIDDEN' 
    default_code = 'The IP address does not exist.'
