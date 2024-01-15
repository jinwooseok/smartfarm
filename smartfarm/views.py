
from django.shortcuts import render, redirect
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
#-----------------------DRF import-----------------------
from .response import *
from .repositorys import *
#-----------------------유틸리티 import-----------------------
from .decorators import logging_time
from .validators import loginValidator
from .utils.FileSystem import FileSystem
from .utils.DataProcess import DataProcess
from .proc import ETL_system
import os
from django.conf import settings

##페이지 별로 필요한 request를 컨트롤
#---------------분석도구 import ----------------
from . import analizer

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view

@api_view(['GET'])
def main_page(request):
    user = loginValidator(request)
    return render(request,'src/Views/Main/main.html')

@api_view(['GET'])
def download_guide(request):
    file_name = 'smartfarm_guidebook.pdf'
    return attach_file(file_name, os.path.join(settings.MEDIA_ROOT, file_name))

def attach_file(file_name, file_path):
    if os.path.exists(file_path):
         with open(file_path, 'rb') as file:
            response = HttpResponse(file.read())
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            return response
    else:
        return JsonResponse(failResponse("파일을 찾을 수 없습니다."), status=400)
