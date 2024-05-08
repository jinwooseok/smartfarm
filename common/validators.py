"""
로그인, request 객체 등의 유효성 검사를 위한 함수를 모아놓은 파일입니다.
"""
from rest_framework import exceptions
from common.validate_exception import ValidationException

def serializer_validator(serializer):
    """
    설명
        serializer의 유효성 검사를 위한 함수
    매개변수
        serializer : serializer 객체
    반환값
        serializer : 유효성 검사 결과
        raise ValidationException(serializer) : 유효성 검사 실패 시 예외 처리
    """
    if serializer.is_valid():
        return serializer
    else:
        raise ValidationException(serializer)

def login_validator(request):
    """
    설명
        로그인 여부를 확인하기 위한 함수
    매개변수
        request : 요청 객체
    반환값
        user_id : 로그인한 사용자의 아이디
        raise exceptions.NotAuthenticated() : 로그인하지 않은 경우 예외 처리
    """
    user_id = request.session.get('user') #session의 유저 데이터불러오기
    if user_id is None:
        raise exceptions.NotAuthenticated()
    else:
        return user_id
        