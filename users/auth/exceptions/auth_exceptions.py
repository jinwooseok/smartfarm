class EmailDuplicatedException(BaseException):
    status_code = 400
    code = 1001
    default_detail = '이미 존재하는 이메일입니다.'
    default_code = 'email_duplicated'

class UserTelDuplicatedException(BaseException):
    status_code = 400
    code = 1002
    default_detail = '이미 존재하는 전화번호입니다.'
    default_code = 'tel_duplicated'