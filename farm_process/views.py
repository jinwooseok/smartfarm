"""
농업 관련 프로세스 관련 API를 정의한 파일
"""
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from common.response import *
from common.validators import login_validator, serializer_validator
from farm_process.service.farm_process_service import FarmProcessService
from farm_process.service.trans_abms_service import TransABMSService
from farm_process.serializers import FarmProcessSerializer, EnvABMSSerializer
class DataABMSViewSet(viewsets.GenericViewSet):
    """
    ABMS 관련 데이터 뷰셋
    
    메서드
    page : ABMS 페이지를 렌더링한다. SSR (GET)
    process_abms : ABMS 데이터를 처리한다. (POST)
    """
    def page(self, request, file_title):
        """
        ABMS 페이지를 렌더링한다. SSR (GET)
        """
        user_id = request.session.get('user')
        if user_id is None:
            return HttpResponse("""<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');
                                location.href='/users/sign-in/';</script>""")
        return render(request, 'src/Views/ABMS/abms.html')

    def process_abms(self, request, file_title):
        """
        ABMS 데이터를 처리한다. (POST)
        """
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = EnvABMSSerializer(data = data)
        serializer = serializer_validator(serializer)
        TransABMSService.from_serializer(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)

class FarmProcessViewSet(viewsets.GenericViewSet):
    """
    농업 처리 관련 데이터 뷰셋
    """
    def process_farm(self, request, file_title):
        """
        농업 데이터를 처리한다. (POST)
        """
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer:FarmProcessSerializer = FarmProcessSerializer(data = data)
        serializer:FarmProcessSerializer = serializer_validator(serializer)
        FarmProcessService(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)
    