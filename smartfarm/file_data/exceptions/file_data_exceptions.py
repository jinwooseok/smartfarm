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
        
class StandardDuplicateException(CustomBaseException):
    def __init__(self,file_object, column_name):
        self.status_code = 462
        self.code = 462
        self.detail = f'{file_object.file_title}의 {column_name}열에 중복 데이터가 있습니다. 처리 후 병합이 가능합니다.'
        
class YValueDuplicateException(CustomBaseException):
    def __init__(self,value):
        self.status_code = 463
        self.code = 463
        self.detail = f'{value}이 독립변수와 반응변수에 중복되어 있습니다.'
        
class RequiredValueException(CustomBaseException):
    def __init__(self, value):
        self.status_code = 464
        self.code = 464
        self.detail = f'{value} 값이 누락되었습니다.'