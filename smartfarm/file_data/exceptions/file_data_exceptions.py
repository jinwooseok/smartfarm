from common.base_exception import CustomBaseException

class FileNotCompleteException(CustomBaseException):
    def __init__(self):
        self.status_code = 460
        self.code = 460
        self.detail = '전처리가 완료되지 않은 파일입니다.'

class DateConverterException(CustomBaseException):
    def __init__(self):
        self.status_code = 461
        self.code = 461
        self.detail = '날짜 형식으로 변환할 수 없는 열입니다.'