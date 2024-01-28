from rest_framework import viewsets
from django.shortcuts import render
from ..models import File
from rest_framework import exceptions
from .serializers import *
from rest_framework.response import Response
from common.response import *
from ..file.serializers import FileNameSerializer
from common.response import ResponseBody
from .serializers import ProcessOutlierSerializer

from .service.get_file_data_service import GetFileDataService
from .service.get_data_summary_service import GetDataSummaryService
from .service.drop_outlier_service import ProcessOutlierService
from common.validate_exception import ValidationException

class FileDataViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()

    def page(self, request, file_title):
        return render(request, 'src/Views/Revise/revise.html')
      
    def details(self, request, file_title):
        user = request.session.get('user')
        if user is None:
            raise exceptions.NotAuthenticated()
        
        serializer = FileNameSerializer(data={'fileName': file_title})
        
        if serializer.is_valid():
            return Response(ResponseBody.generate(data=GetFileDataService(serializer, user).execute()), status=200)     
    
    def summary(self, request, file_title):
        user = request.session.get('user')
        if user is None:
            raise exceptions.NotAuthenticated()
        
        serializer = FileNameSerializer(data={'fileName': file_title})

        if serializer.is_valid():
            return Response(ResponseBody.generate(data=GetDataSummaryService(serializer, user).execute()), status=200)
        else:
            raise ValidationException()
    
    def process_outlier(self, request, file_title):
        user = request.session.get('user')
        if user is None:
            raise exceptions.NotAuthenticated()
        
        serializer = ProcessOutlierSerializer(data=request.data)
        serializer.initial_data['fileName'] = file_title

        if serializer.is_valid():
            ProcessOutlierService.from_serializer(serializer, user).execute()
            return Response(ResponseBody.generate(), status=200)
    
    def process_time_series():
        return 0

class DataMergeViewSet(viewsets.GenericViewSet):
    def page(self, request):
        return render(request, 'src/Views/Merge/merge.html')