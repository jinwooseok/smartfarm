from rest_framework.exceptions import APIException
from rest_framework import status
class CustomBaseException(APIException):
    def __init__(self, detail=None, code=None, status_code=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = "Unknown Error"
        if code is not None:
            self.code = code
        else:
            self.code = 500
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
