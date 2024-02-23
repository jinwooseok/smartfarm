from common.base_exception import CustomBaseException

class ModelTypeException(CustomBaseException):
    def __init__(self, value, type):
        self.status_code = 480
        self.code = 480
        self.detail = f'{value} 변수 타입이 {type}입니다.'