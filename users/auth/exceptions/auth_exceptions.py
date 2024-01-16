from rest_framework import status
from common.base_exception import CustomBaseException
#회원가입
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

#로그인
class IdNotFoundException(CustomBaseException):
    def __init__(self):
        self.status_code = 404
        self.code = 1001
        self.detail = '존재하지 않는 이메일입니다.'

class PasswordNotMatchedException(CustomBaseException):
    def __init__(self):
        self.status_code = 400
        self.code = 1002
        self.detail = '비밀번호가 일치하지 않습니다.'