from django.shortcuts import render, redirect, get_object_or_404
from ..models import User
from argon2 import PasswordHasher
from django.contrib.auth import authenticate
from argon2.exceptions import VerifyMismatchError
from rest_framework import exceptions,viewsets
from .serializers import *
from rest_framework.response import Response
from .exceptions.auth_exceptions import *
from common.base_exception import CustomBaseException
from drf_yasg.utils import swagger_auto_schema
class SignUpViewSet(viewsets.GenericViewSet):
    def page(self, request):
        #이미 로그인한 사람이라면 이용 불가
        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()
        #로그인 하지 않았다면 페이지 렌더링
        return render(request, 'src/Views/Register/register.html')
    
    @swagger_auto_schema(request_body=SignUpSerializer, responses={1001: '이메일 중복', 1002: '전화번호', 500: '서버 에러'})
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()
        if serializer.is_valid():
            #이메일 중복 확인
            if self.is_duplicated_email(serializer.validated_data['user_id']):
                raise EmailDuplicatedException()
            #비밀번호 암호화
            serializer.validated_data['user_pw'] = PasswordHasher().hash(serializer.validated_data['user_pw'])
            #전화번호 합체
            serializer.validated_data['user_tel'] = ''.join(serializer.validated_data['user_tel'])
            #전화번호 검증
            if self.is_duplicated_user_tel(serializer.validated_data['user_tel']):
                raise UserTelDuplicatedException()
            #DB에 저장
            serializer.save()
            return Response(serializer.success(),status=201)
            #비밀번호는 argon2의 hash함수를 사용해 db에 저장
        else:
            raise exceptions.ValidationError()
    
    @swagger_auto_schema(request_body=EmailValidationSerializer)
    def valid_email(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            if self.is_duplicated_email(serializer.validated_data['email']):
                raise EmailDuplicatedException()

            return Response(serializer.success(),status=200)
        else:
            raise exceptions.ValidationError()
    #내부 사용 함수
    def is_duplicated_user_tel(self, user_tel):
        return User.objects.filter(user_tel=user_tel).exists()
    
    def is_duplicated_email(self, email):
        return User.objects.filter(user_id=email).exists()


class SignInViewSet(viewsets.GenericViewSet):
    def page(self, request):
        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()
        return render(request, 'src/Views/Login/login.html')
    
    @swagger_auto_schema(request_body=SignInSerializer)
    def sign_in(self, request):
        serializer = SignInSerializer(data=request.data)

        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()

        if serializer.is_valid():
            try:
                user = User.objects.get(user_id=serializer.validated_data['email'])
            except User.DoesNotExist:
                raise IdNotFoundException()
            
            try:
                self.is_correct_password(user.user_pw, serializer.validated_data['password'])
            except VerifyMismatchError:    
                raise PasswordNotMatchedException()

            request.session['user'] = user.id
            print(serializer.success())
            return Response(serializer.success(),status=200)
        
        else:
            raise exceptions.ValidationError()
        
    def is_correct_password(self, login_pw, user_pw):
        return PasswordHasher().verify(login_pw.encode(), user_pw.encode())
        

class SignOutViewSet(viewsets.GenericViewSet):
    def sign_out(self, request):
        login_session = request.session.get('user', None)

        if login_session is None:
            raise exceptions.NotAuthenticated()
        
        request.session.flush()
        return Response({"status":"success","message":"로그아웃에 성공했습니다."},status=200)

