from .base_exception import CustomBaseException

class ValidationException(CustomBaseException):
    def __init__(self, serializer):
        # 유효성 검사가 실패한 경우
        errors = serializer.errors
        value_list = []
        for field, error_list in errors.items():
            for error in error_list:
                value_list.append(f'{field}: {error}')
        self.status_code = 400
        self.code = 400
        self.detail =  value_list.__str__()
        