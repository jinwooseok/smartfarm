from common.base_exception import CustomBaseException

class FileNotCompleteException(CustomBaseException):
    def __init__(self):
        self.status_code = 452
        self.code = 452
        self.detail = '전처리가 완료되지 않은 파일입니다.'
