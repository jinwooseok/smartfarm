"""
공통 유효성 검사 실패 예외 처리 클래스. base_exception.CustomBaseException을 상속받아 구현한다.
"""
from common.base_exception import CustomBaseException

class ValidationException(CustomBaseException):
    """
    설명
        유효성 검사 실패 예외 처리 클래스
    """
    def __init__(self, serializer):
        super().__init__()
        # 유효성 검사가 실패한 경우 serializer 클래스의 errors 속성을 참조하여 에러 메시지를 생성한다.
        errors = serializer.errors
        value_list = []
        for field, error_list in errors.items():
            for error in error_list:
                if error == "This field is required.":
                    value_list.append(f"({field}) : 필수 {field}에 값이 존재하지 않습니다.")
                else:
                    value_list.append(f"({field}) : 유효하지 않은 {field}입니다.")
        self.status_code = 400
        self.code = 400
        self.detail =  ", ".join(value_list)
        