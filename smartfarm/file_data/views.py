from rest_framework import viewsets
from django.shortcuts import render
from ..models import File
from .serializers import *
from django.http import HttpResponse
from rest_framework.response import Response
from common.response import *
from ..file.serializers import FileNameSerializer
from common.response import ResponseBody
from .serializers import ProcessOutlierSerializer

from .service.merge_data_service import MergeDataService
from .service.get_file_data_service import GetFileDataService
from .service.get_data_summary_service import GetDataSummaryService
from .service.drop_outlier_service import ProcessOutlierService
from .service.shift_data_service import ShiftDataService
from common.validators import serializer_validator, login_validator

class FileDataViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()

    def page(self, request, file_title):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/Revise/revise.html')
      
    def details(self, request, file_title):
        user_id = login_validator(request)
        
        serializer = FileNameSerializer(data={'fileName': file_title})
        
        serializer = serializer_validator(serializer)
        return Response(ResponseBody.generate(
            data=GetFileDataService.from_serializer(serializer, user_id).execute()), status=200)     
    
    def summary(self, request, file_title):
        user_id = login_validator(request)
        
        serializer = FileNameSerializer(data={'fileName': file_title})

        serializer = serializer_validator(serializer)
        
        return Response(ResponseBody.generate(
            data=GetDataSummaryService(serializer, user_id).execute()), status=200)
    
    def process_outlier(self, request, file_title):
        user_id = login_validator(request)
        
        serializer = ProcessOutlierSerializer(data=request.data)
        serializer.initial_data['fileName'] = file_title

        serializer = serializer_validator(serializer)
        
        return Response(ResponseBody.generate(
            data=ProcessOutlierService.from_serializer(serializer, user_id).execute()), status=200)

        
    def process_time_series(self, request, file_title):
        user_id = login_validator(request)
        
        data = request.data.copy()
        data['fileName'] = file_title
        data['feature']=data['feature[]']
        serializer = ProcessTimeSeriesSerializer(data=data)

        serializer = serializer_validator(serializer)
        ShiftDataService.from_serializer(serializer, user_id).execute()
        return Response(ResponseBody.generate(), status=200)

class DataMergeViewSet(viewsets.GenericViewSet):
    def page(self, request):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/Merge/merge.html')
    
    def merge(self, request):
        user_id = login_validator(request)
        serializer = DataMergeSerializer(data=request.data)
        serializer = serializer_validator(serializer)
        return Response(ResponseBody.generate(
            data=MergeDataService.from_serializer(serializer, user_id).execute()), status=200)