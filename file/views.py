from rest_framework import viewsets
from django.shortcuts import render
from file.serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
from file.repositorys import filter_file_by_user
from common.response import *
from file.service.file_save_service import FileSaveService
from file.service.file_delete_service import FileDeleteService
from file_data.service.get_file_data_service import GetFileDataService
from common.validators import login_validator, serializer_validator

#파일 관련 뷰셋
class FileViewSet(viewsets.GenericViewSet):
    def page(self, request):
        user_id = request.session.get('user')
        if user_id == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n로그인 페이지로 돌아갑니다.');location.href='/users/sign-in/';</script>")
        return render(request, 'src/Views/FileList/fileList.html')

    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        user_id = login_validator(request)
        file_object = filter_file_by_user(user_id)
        file_object = paginator.paginate_queryset(file_object, request)
        serializer = FileInfoSerializer(file_object, many=True)
        return Response(ResponseBody.generate(serializer=serializer), status=200)
        
    def name_list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user_id = login_validator(request)
        file_object = filter_file_by_user(user_id)
        file_object = paginator.paginate_queryset(file_object, request)
        serializer = FileNameModelSerializer(file_object, many=True)
        return Response(ResponseBody.generate(serializer=serializer), status=200)
    
    def save(self, request):
        user_id = login_validator(request)
        serializer = FileSaveSerializer(data=request.data)
        serializer = serializer_validator(serializer)
        FileSaveService.from_serializer(serializer, user_id).execute()
        
        return Response(ResponseBody.generate(),status=201)

    
    def delete(self, request):
        user_id = login_validator(request)
        
        serializer = FileDeleteSerializer(data=request.data)

        serializer = serializer_validator(serializer)
        
        FileDeleteService.from_serializer(serializer, user_id).execute()
        
        return Response(ResponseBody.generate(),status=200)
    
    def download(self, request):
        user_id = login_validator(request)
        
        serializer = FileNameSerializer(data=request.data)
        
        serializer = serializer_validator(serializer)
        
        return Response(ResponseBody.generate(data=GetFileDataService.from_serializer(serializer, user_id).execute()), status=200)  

