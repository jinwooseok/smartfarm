from rest_framework import status
from common.base_exception import CustomBaseException
class EmailDuplicatedException(CustomBaseException):
    def __init__(self):
        self.status_code = 400
        self.code = 1001
        self.detail = '이미 존재하는 이메일입니다.'

class UserTelDuplicatedException(CustomBaseException):
    def __init__(self):
        self.status_code = 400
        self.code = 1002
        self.detail = '이미 존재하는 전화번호입니다.'