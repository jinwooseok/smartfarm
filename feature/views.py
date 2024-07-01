from rest_framework import viewsets
from feature.models import FileFeature
from file.models import File
from rest_framework.response import Response
from common.response import *
from .serializers import FileFeatureSerializer, GetFeatureImportanceSerializer
from .service.feature_importance_service import FeatureImportanceService
from common.validators import login_validator, serializer_validator
class FeatureViewSet(viewsets.ModelViewSet):
    """
    feature에 대한 API View
    
    Attributes
    ----------
    queryset : QuerySet
        FileFeature 모델의 모든 인스턴스
        
    Methods
    -------
    feature_list : feature 리스트 반환
    feature_importance : feature 중요도 반환
    create_feature_importance : feature 중요도 생성
    """
    queryset = FileFeature.objects.all()

    def feature_list(self, request, file_title):
        user_id = login_validator(request)
        file_object = File.objects.get(user_id=user_id,file_title=file_title)
        queryset = FileFeature.objects.filter(file=file_object)
        serializer = FileFeatureSerializer(queryset, many=True)
        return Response(ResponseBody.generate(serializer=serializer), status=200)

    def feature_importance(self, request, file_title):
        user_id = login_validator(request)
        file_object = File.objects.get(user_id=user_id,file_title=file_title)
        queryset = FileFeature.objects.filter(file=file_object)
        serializer = FileFeatureSerializer(queryset.order_by('-feature_importance'), many=True)
        return Response(ResponseBody.generate(serializer=serializer), status=200)
    def create_feature_importance(self, request, file_title):
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = GetFeatureImportanceSerializer(data=data)
        serializer = serializer_validator(serializer)
        return Response(ResponseBody.generate(data=FeatureImportanceService.from_serializer(serializer, user_id).execute()), status=200)