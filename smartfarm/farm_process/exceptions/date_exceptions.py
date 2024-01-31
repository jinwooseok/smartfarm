from common.base_exception import CustomBaseException

class NullDateException(CustomBaseException):
    def __init__(self):
        self.status_code = 452
        self.code = 452
        self.detail = '날짜열에 null값이 존재합니다. 결측치를 제거해주세요.'

class GetSunApiException(CustomBaseException):
    def __init__(self):
        self.status_code = 453
        self.code = 453
        self.detail = '날씨 API를 가져오는데 실패하였습니다. 다시 시도해주세요.'