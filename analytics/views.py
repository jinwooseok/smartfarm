"""
데이터 분석 관련 컨트롤러(뷰셋)를 정의한 파일
"""
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from common.validators import login_validator, serializer_validator
from .service.create_model_service import CreateModelService
from .service.download_model_service import DownloadModelService
from .service.predict_model_service import PredictModelService
from .serializers import *
from common.response import *
#데이터 분석 관련 뷰셋
class DataAnalyticsViewSet(viewsets.GenericViewSet):
    """
    데이터 분석 관련 뷰셋 (서비스와 직접적인 연결을 담당한다.)
    """
    def page(self, request, file_title):
        """
        데이터 분석 페이지를 렌더링한다. SSR (GET)
        
        서비스 로직
        1. 사용자가 업로드한 데이터를 받는다.
        2. 데이터를 렌더링한다.
        3. 렌더링된 페이지를 반환한다.
        """
        user_id = request.session.get('user')
        if user_id is None:
            return HttpResponse("""<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');
                                location.href='/users/sign-in/';</script>""")
        return render(request, 'src/Views/Analyze/analyze.html')

    def create_model(self, request, file_title):
        """
        모델을 생성한다. (POST)
        
        서비스 로직
        1. 사용자가 업로드한 데이터를 받는다.
        2. 모델을 생성한다.
        3. 모델을 저장한다.
        4. 모델 메타 정보를 저장한다.
        5. 모델정보를 반환한다.
        """
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = CreateModelSerializer(data=data)
        serializer = serializer_validator(serializer)
        return Response(ResponseBody.generate(
            data=CreateModelService.from_serializer(serializer, user_id).execute()),status=201)

    def download_model(self, request, model_title):
        """
        모델을 다운로드 한다. (GET)
        
        서비스 로직
        1. 모델을 찾는다.
        2. 모델을 다운로드한다.
        3. 다운로드한 모델을 반환한다.
        """
        user_id = login_validator(request)
        data = request.data.copy()
        data['modelName'] = model_title
        serializer = ModelNameSerializer(data=data)
        serializer = serializer_validator(serializer)
        return DownloadModelService.from_serializer(serializer, user_id).execute()

    def predict(self, request, model_title):
        """
        모델을 예측한다. (POST)
        
        서비스 로직
        1. 모델을 찾는다.
        2. 모델을 예측한다.
        3. 예측 결과를 반환한다.
        """
        user_id = login_validator(request)
        data = request.data.copy()
        data['modelName'] = model_title
        serializer = ModelNameSerializer(data=data)
        serializer = serializer_validator(serializer)
        return Response(ResponseBody.generate(
            data=PredictModelService.from_serializer(serializer, user_id).execute()),status=200)
