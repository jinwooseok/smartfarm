from rest_framework import serializers
from ..models import User
class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    job = serializers.CharField(required=True)
    phone = serializers.ListField(required=True)

    def save(self):
        user = User(
            user_id=self.validated_data['email'],
            user_pw=self.validated_data['password'],
            user_name=self.validated_data['name'],
            user_tel=self.validated_data['phone'],
            user_job=self.validated_data['job']
        )
        user.save()
    
    def success(self):
        return {"status":"success","message":"회원가입에 성공했습니다."}
    
class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def success(self):
        return {"status":"success","message":"중복되지 않는 이메일입니다."}

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    def success(self):
        return {"status":"success","message":"로그인에 성공했습니다."}