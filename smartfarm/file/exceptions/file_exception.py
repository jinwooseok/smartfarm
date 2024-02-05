from common.base_exception import CustomBaseException

class FileNotFoundException(CustomBaseException):
    def __init__(self):
        self.status_code = 452
        self.code = 452
        self.detail = 'DB에 파일이 존재하지 않습니다.'

class OriginalFileNotFoundException(CustomBaseException):
    def __init__(self):
        self.status_code = 453
        self.code = 453
        self.detail = '원본 파일이 존재하지 않습니다.'

class FileSaveException(CustomBaseException):
    def __init__(self):
        self.status_code = 454
        self.code = 454
        self.detail = '파일 저장에 실패하였습니다.'
        
class TempNotFoundException(CustomBaseException):
    def __init__(self):
        self.status_code = 455
        self.code = 455
        self.detail = '저장된 임시파일이 없습니다.'
        
class DataToCsvException(CustomBaseException):
    def __init__(self):
        self.status_code = 456
        self.code = 456
        self.detail = 'csv파일로 변환할 수 없는 데이터입니다.'