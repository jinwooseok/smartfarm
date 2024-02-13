from rest_framework import viewsets
from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from common.response import *
from django.http import HttpResponse
from common.validators import login_validator, serializer_validator
from .service.create_model_service import CreateModelService
#데이터 분석 관련 뷰셋
class DataAnalyticsViewSet(viewsets.GenericViewSet):
    
    def page(self, request, file_title):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/Analyze/analyze.html')
    
    def create_model(self, request, file_title):
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = CreateModelSerializer(data=request.data)
        serializer = serializer_validator(serializer)
        CreateModelService.from_serializer(serializer, user_id).execute()
        return Response(ResponseBody.generate(),status=201)