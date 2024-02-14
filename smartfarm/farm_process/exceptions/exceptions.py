from common.base_exception import CustomBaseException

class NullDateException(CustomBaseException):
    def __init__(self):
        self.status_code = 470
        self.code = 470
        self.detail = '날짜열에 null값이 존재합니다. 결측치를 제거해주세요.'

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
        