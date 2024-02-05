from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from common.response import *
from common.validators import login_validator, serializer_validator
from .service.farm_process_service import FarmProcessService
from common.validate_exception import ValidationException
from .serializers import FarmProcessSerializer
class DataABMSViewSet(viewsets.GenericViewSet):
    def page(self, request, file_title):
        return render(request, 'src/Views/ABMS/abms.html')
    
class FarmProcessViewSet(viewsets.GenericViewSet):
    
    def process_farm(self, request, file_title):
        user_id = login_validator(request)
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = FarmProcessSerializer(data = data)
        serializer = serializer_validator(serializer)
        data=FarmProcessService(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)
    