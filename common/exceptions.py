"""
시스템 상 모든 예외를 정의한 파일. 452~499까지의 코드를 사용한다.
"""
from common.base_exception import CustomBaseException
class FileNotFoundException(CustomBaseException):
    """
    설명
        DB상 파일 정보를 찾을 수 없을 때 발생하는 오류. 코드 452
    """
    def __init__(self):
        super().__init__()
        self.status_code = 452
        self.code = 452
        self.detail = 'DB에 파일이 존재하지 않습니다.'

class OriginalFileNotFoundException(CustomBaseException):
    """
    설명
        로컬 파일 시스템(media 폴더)에 원본 파일을 찾을 수 없을 때 발생하는 오류. 코드 453
    """
    def __init__(self):
        super().__init__()
        self.status_code = 453
        self.code = 453
        self.detail = '원본 파일이 존재하지 않습니다.'

class FileSaveException(CustomBaseException):
    """
    설명
        파일 저장에 실패했을 때 발생하는 오류. 코드 454
    """
    def __init__(self):
        super().__init__()
        self.status_code = 454
        self.code = 454
        self.detail = '파일 저장에 실패하였습니다.'

class TempNotFoundException(CustomBaseException):
    """
    설명
        임시파일을 찾을 수 없을 때(media/{user_id}/temp/) 발생하는 오류. 코드 455
    """
    def __init__(self):
        super().__init__()
        self.status_code = 455
        self.code = 455
        self.detail = '저장된 임시파일이 없습니다.'

class DataToCsvException(CustomBaseException):
    """
    설명
        데이터를 csv파일로 변환할 수 없을 때 발생하는 오류. 코드 456
    """
    def __init__(self):
        super().__init__()
        self.status_code = 456
        self.code = 456
        self.detail = 'csv파일로 변환할 수 없는 데이터입니다.'

class DateColumnException(CustomBaseException):
    """
    설명
        처음 파일 업로드 시 날짜열이 설정되지 않았을 때 발생하는 오류. 코드 457
    """
    def __init__(self):
        super().__init__()
        self.status_code = 457
        self.code = 457
        self.detail = '날짜열이 설정되지 않았습니다.'

class FileNotCompleteException(CustomBaseException):
    """
    설명
        전처리가 완료되지 않은 파일을 분석하려고 할 때 발생하는 오류. 코드 460
    """
    def __init__(self):
        super().__init__()
        self.status_code = 460
        self.code = 460
        self.detail = '전처리가 완료되지 않은 파일입니다.'

#------------------데이터 관련 오류------------------
class DateConverterException(CustomBaseException):
    """
    설명
        날짜 형식으로 변환할 수 없는 열을 변환하려는 경우 발생하는 오류. 코드 461
    """
    def __init__(self):
        super().__init__()
        self.status_code = 461
        self.code = 461
        self.detail = '날짜 형식으로 변환할 수 없는 열입니다.'

class StandardDuplicateException(CustomBaseException):
    """
    설명
        병합할 때 중복 데이터가 존재할 경우 발생하는 오류. 코드 462
    """
    def __init__(self,file_object, column_name):
        super().__init__()
        self.status_code = 462
        self.code = 462
        self.detail = f'{file_object.file_title}의 {column_name}열에 중복 데이터가 있습니다. 처리 후 병합이 가능합니다.'

class YValueDuplicateException(CustomBaseException):
    """
    설명
        독립변수와 반응변수에 중복되는 열이 존재할 경우 발생하는 오류. 코드 463
    """
    def __init__(self,value):
        super().__init__()
        self.status_code = 463
        self.code = 463
        self.detail = f'{value}이 독립변수와 반응변수에 중복되어 있습니다.'

class RequiredValueException(CustomBaseException):
    """
    설명
        요청 시 필수값이 누락되었을 때 발생하는 오류. 코드 464
    """
    def __init__(self, value):
        super().__init__()
        self.status_code = 464
        self.code = 464
        self.detail = f'{value} 값이 누락되었습니다.'

class NullDateException(CustomBaseException):
    """
    설명
        날짜열에 null값이 존재할 때 발생하는 오류. 코드 470
    """
    def __init__(self):
        super().__init__()
        self.status_code = 470
        self.code = 470
        self.detail = '날짜열에 null값이 존재합니다. 결측치를 제거해주세요.'

#------------------농업 데이터 관련 오류------------------
class GetSunApiException(CustomBaseException):
    """
    설명
        날씨 API를 호출하는데 실패했을 때 발생하는 오류. API키가 만료된 경우에도 발생함. 코드 471
    """
    def __init__(self):
        super().__init__()
        self.status_code = 471
        self.code = 471
        self.detail = '날씨 API를 가져오는데 실패하였습니다. 잠시 후 다시 시도해주세요.'

class StartIndexException(CustomBaseException):
    """
    설명
        시작행이 1보다 작거나 데이터 길이를 초과할 때 발생하는 오류. 코드 472
    """
    def __init__(self):
        super().__init__()
        self.status_code = 472
        self.code = 472
        self.detail = '시작행이 1보다 작거나 데이터 길이를 초과합니다.'

class VarDataException(CustomBaseException):
    """
    설명
        변수 데이터에서 발생한 오류. 코드 473
    """
    def __init__(self, variable):
        super().__init__()
        self.status_code = 474
        self.code = 474
        self.detail = f'{variable} 변수에서 오류가 발생했습니다.'

class ModelTypeException(CustomBaseException):
    """
    설명
        모델에 맞지 않는 변수 타입(범주형 or 이산형)을 사용했을 경우 발생하는 오류. 코드 480
    """
    def __init__(self, value, data_type):
        super().__init__()
        self.status_code = 480
        self.code = 480
        self.detail = f'{value} 변수 타입이 {data_type}입니다.'

#------------------분석 관련 오류------------------        
class DataCountException(CustomBaseException):
    """
    설명
        관측치 개수가 너무 적을 때 발생하는 오류. 코드 481
    """
    def __init__(self, x_count, data_count):
        super().__init__()
        self.status_code = 481
        self.code = 481
        self.detail = f'관측치 개수가 너무 적습니다. x:{x_count}, 관측치 수:{data_count}'

class InvalidFeatureException(CustomBaseException):
    """
    설명
        분석에 필요한 변수가 유효하지 않을 때 발생하는 오류. 코드 482
    
    """
    def __init__(self, value):
        super().__init__()
        self.status_code = 482
        self.code = 482
        self.detail = f'{value} 변수가 존재하지 않습니다.'