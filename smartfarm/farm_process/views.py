from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from common.response import *
from rest_framework import exceptions
from ..file.serializers import FileNameSerializer
from .service.farm_process_service import FarmProcessService
from common.validate_exception import ValidationException
from .serializers import FarmProcessSerializer
class DataABMSViewSet(viewsets.GenericViewSet):
    def page(self, request, file_title):
        return render(request, 'src/Views/ABMS/abms.html')
    
class FarmProcessViewSet(viewsets.GenericViewSet):
    
    def process_farm(self, request, file_title):
        user = request.session.get('user')
        if user is None:
            raise exceptions.NotAuthenticated()
        data = request.data.copy()
        data['fileName'] = file_title
        serializer = FarmProcessSerializer(data = data)
        
        if serializer.is_valid():
            data=FarmProcessService(serializer, user).execute()
            return Response(ResponseBody.generate(), status=200)
        else:
            raise ValidationException(serializer)
    