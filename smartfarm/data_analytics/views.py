from rest_framework import viewsets
from django.shortcuts import render
from ..models import File
from rest_framework import exceptions
from .serializers import *
from rest_framework.response import Response
from common.response import *
from common.validate_exception import ValidationException
from django.http import HttpResponse
#데이터 분석 관련 뷰셋
class DataAnalyticsViewSet(viewsets.GenericViewSet):
    
    def page(self, request, file_title):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/Analyze/analyze.html')