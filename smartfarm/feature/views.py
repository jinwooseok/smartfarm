from rest_framework import viewsets
from ..models import FileFeature, File
from rest_framework.response import Response
from common.response import *
from .serializers import FileFeatureSerializer
from common.validators import login_validator
class FeatureViewSet(viewsets.ModelViewSet):
    
    queryset = FileFeature.objects.all()
    
    def feature_list(self, request, file_title):
        user_id = login_validator(request)
        file_object = File.objects.get(user_id=user_id,file_title=file_title)
        queryset = FileFeature.objects.filter(file=file_object)
        serializer = FileFeatureSerializer(queryset, many=True)
        return Response(ResponseBody.generate(serializer=serializer), status=200)
        