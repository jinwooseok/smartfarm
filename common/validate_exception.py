from .base_exception import CustomBaseException

class ValidationException(CustomBaseException):
    def __init__(self, serializer):
        # 유효성 검사가 실패한 경우
        errors = serializer.errors
        value_list = []
        for field, error_list in errors.items():
            for error in error_list:
                if (error == "This field is required."):
                    value_list.append(f"({field}) : 필수 {field}에 값이 존재하지 않습니다.")
                else:
                    value_list.append(f"({field}) : 유효하지 않은 {field}입니다.")
        self.status_code = 400
        self.code = 400
        self.detail =  ", ".join(value_list)
        