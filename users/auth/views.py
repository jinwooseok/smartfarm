from django.shortcuts import render, redirect
from ..models import User
from argon2 import PasswordHasher
from django.contrib.auth import authenticate
from argon2.exceptions import VerifyMismatchError
from rest_framework import exceptions,viewsets
from .serializers import SignUpSerializer, EmailValidationSerializer
from rest_framework.response import Response
from .exceptions.auth_exceptions import *
from common.base_exception import CustomBaseException
from drf_yasg.utils import swagger_auto_schema
class SignUpViewSet(viewsets.GenericViewSet):
    def page(self, request):
        #이미 로그인한 사람이라면 이용 불가
        if authenticate(request) is not None:
            raise exceptions.NotAcceptable()
        #로그인 하지 않았다면 페이지 렌더링
        return render(request, 'src/Views/Register/register.html')
    
    @swagger_auto_schema(request_body=SignUpSerializer, responses={1001: '이메일 중복', 1002: '전화번호', 500: '서버 에러'})
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
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
            return Response({"status":"success","message":"회원가입에 성공했습니다."},status=201)
            #비밀번호는 argon2의 hash함수를 사용해 db에 저장
        else:
            raise exceptions.ValidationError()
    
    @swagger_auto_schema(request_body=EmailValidationSerializer)
    def valid_email(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            if self.is_duplicated_email(serializer.validated_data['email']):
                raise EmailDuplicatedException()
            return Response({"status":"success","message":"중복되지 않는 이메일입니다."},status=200)
        else:
            raise exceptions.ValidationError()
    #내부 사용 함수
    def is_duplicated_user_tel(self, user_tel):
        if User.objects.filter(user_tel=user_tel).exists():
            return True
        return False
    
    def is_duplicated_email(self, email):
        if User.objects.filter(user_id=email).exists():
            return True
        return False

class SignInViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def page(self, request):
        #이미 로그인한 사람이라면 이용 불가
        if authenticate(request) is not None:
            raise exceptions.NotAcceptable()
        return render(request, 'src/Views/Login/login.html')
    
    def sign_in(self, request):
        if request.session.get('user'):
            return redirect('/')

        login_user_id=request.POST['id']
        login_user_pw=request.POST['password']

        try:
            user = User.objects.get(user_id=login_user_id)
        except User.DoesNotExist:
            user=None
            context = {
                'error' : '계정이 존재하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        try :
            PasswordHasher().verify(user.user_pw.encode(), login_user_pw.encode())
        except VerifyMismatchError:
            user=None  
            context = {
                'error' : '비밀번호가 일치하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        if user != None:
            request.session['user'] = user.id
        
            # Redirect to a success page.
            return redirect('/')
            
        else:
            context = {
                'error' : '로그인에 실패하였습니다.'
            }
            return render(request, 'Html/login.html', context)

class SignOutViewSet(viewsets.ModelViewSet):
        
    queryset = User.objects.all()

    def sign_out(self, request):
        request.session.flush()
        return redirect('/')
