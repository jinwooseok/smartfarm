from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse

from common.response import *
from common.validators import login_validator, serializer_validator
from .service.farm_process_service import FarmProcessService
from .service.trans_abms_service import TransABMSService
from .serializers import FarmProcessSerializer, EnvABMSSerializer
class DataABMSViewSet(viewsets.GenericViewSet):
    def page(self, request, file_title):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/ABMS/abms.html')
    
    def process_abms(self, request, file_title):
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = EnvABMSSerializer(data = data)
        serializer = serializer_validator(serializer)
        data=TransABMSService.from_serializer(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)
    
class FarmProcessViewSet(viewsets.GenericViewSet):
    
    def process_farm(self, request, file_title):
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer:FarmProcessSerializer = FarmProcessSerializer(data = data)
        serializer:FarmProcessSerializer = serializer_validator(serializer)
        data=FarmProcessService(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)
    