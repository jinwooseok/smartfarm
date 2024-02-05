from django.shortcuts import render
from rest_framework import exceptions,viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from common.response import ResponseBody
from .serializers import *
from .exceptions.auth_exceptions import *
from .service.save_user_service import SaveUserService
from .service.auth_user_service import AuthUserService
from common.validators import serializer_validator
class SignUpViewSet(viewsets.GenericViewSet):
    def page(self, request):
        #로그인 하지 않았다면 페이지 렌더링
        return render(request, 'src/Views/Register/register.html')
    
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()
        
        serializer = serializer_validator(serializer)
        SaveUserService.from_serializer(serializer).execute()
        return Response(ResponseBody.generate(),status=201)
    
    @swagger_auto_schema(request_body=EmailValidationSerializer)
    def valid_email(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        serializer = serializer_validator(serializer)
        if SaveUserService.is_duplicated_email(serializer.validated_data['email']):
            raise EmailDuplicatedException()
        return Response(ResponseBody.generate(),status=200)

class SignInViewSet(viewsets.GenericViewSet):
    def page(self, request):
        return render(request, 'src/Views/Login/login.html')
    
    @swagger_auto_schema(request_body=SignInSerializer)
    def sign_in(self, request):
        serializer = SignInSerializer(data=request.data)

        if request.session.get('user') is not None:
            raise exceptions.PermissionDenied()

        serializer = serializer_validator(serializer)
        user = AuthUserService.from_serializer(serializer).execute()
        request.session['user'] = user.id
        return Response(ResponseBody.generate(),status=200)

class SignOutViewSet(viewsets.GenericViewSet):
    def sign_out(self, request):
        request.session.flush()
        return Response(ResponseBody.generate(),status=200)

