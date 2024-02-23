from common.base_exception import CustomBaseException
        
class DataCountException(CustomBaseException):
    def __init__(self, x_count, data_count):
        self.status_code = 481
        self.code = 481
        self.detail = f'관측치 개수가 너무 적습니다. x:{x_count}, 관측치 수:{data_count}'