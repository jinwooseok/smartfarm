from common.base_exception import CustomBaseException
#------------------파일 관련 오류------------------
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
        
class DateColumnException(CustomBaseException):
    def __init__(self):
        self.status_code = 457
        self.code = 457
        self.detail = '날짜열이 설정되지 않았습니다.'
class FileNotCompleteException(CustomBaseException):
    def __init__(self):
        self.status_code = 460
        self.code = 460
        self.detail = '전처리가 완료되지 않은 파일입니다.'
#------------------데이터 관련 오류------------------
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
        
class NullDateException(CustomBaseException):
    def __init__(self):
        self.status_code = 470
        self.code = 470
        self.detail = '날짜열에 null값이 존재합니다. 결측치를 제거해주세요.'
#------------------농업 데이터 관련 오류------------------
class GetSunApiException(CustomBaseException):
    def __init__(self):
        self.status_code = 471
        self.code = 471
        self.detail = '날씨 API를 가져오는데 실패하였습니다. 잠시 후 다시 시도해주세요.'
        
class StartIndexException(CustomBaseException):
    def __init__(self):
        self.status_code = 472
        self.code = 472
        self.detail = '시작행이 1보다 작거나 데이터 길이를 초과합니다.'
        
class VarDataException(CustomBaseException):
    def __init__(self, variable):
        self.status_code = 474
        self.code = 474
        self.detail = f'{variable} 변수에서 오류가 발생했습니다.'

class ModelTypeException(CustomBaseException):
    def __init__(self, value, type):
        self.status_code = 480
        self.code = 480
        self.detail = f'{value} 변수 타입이 {type}입니다.'
#------------------분석 관련 오류------------------        
class DataCountException(CustomBaseException):
    def __init__(self, x_count, data_count):
        self.status_code = 481
        self.code = 481
        self.detail = f'관측치 개수가 너무 적습니다. x:{x_count}, 관측치 수:{data_count}'
        
class InvalidFeatureException(CustomBaseException):
    def __init__(self, value):
        self.status_code = 482
        self.code = 482
        self.detail = f'{value} 변수가 존재하지 않습니다.'