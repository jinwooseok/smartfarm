from .validate_exception import ValidationException
from rest_framework import exceptions

def serializer_validator(serializer):
    if serializer.is_valid():
        return serializer
    else:
        raise ValidationException(serializer)
    
def login_validator(request):
    user_id = request.session.get('user')#session데이터불러오기
    if user_id is None:
            raise exceptions.NotAuthenticated()
    else: 
        return user_id #None을 반환하면 페이지 이동 시 None소유 템플릿에서 if문 처리 가능
        