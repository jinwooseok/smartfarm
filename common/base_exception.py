'''
APIException : REST framework에서 제공하는 예외 클래스. 상속하여 사용
status : REST framework에서 제공하는 HTTP 상태 코드를 정의하는 객체
'''
from rest_framework.exceptions import APIException
from rest_framework import status
class CustomBaseException(APIException):
    '''
    커스텀 예외들의 기반이 되는 코드
    
    매개변수:
        detail (str): 예외의 상세 설명
        code (int): 예외의 구체적 상태 코드
        status_code (int): HTTP 상태 코드
    '''
    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail)
        if code is not None:
            self.code = code
        else:
            self.code = 500
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
