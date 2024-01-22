from rest_framework import viewsets
from django.shortcuts import render
from ..models import File
from rest_framework import exceptions
from .serializers import *
from rest_framework.response import Response
from common.response import *
from common.validate_exception import ValidationException

#데이터 분석 관련 뷰셋
class DataAnalyticsViewSet(viewsets.GenericViewSet):
    
    def page(self, request, file_title):
        return render(request, 'src/Views/Analyze/analyze.html')