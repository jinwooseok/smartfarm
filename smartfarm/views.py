
from django.shortcuts import render

#-----------------------유틸리티 import-----------------------
from .decorators import logging_time
from .validators import loginValidator
import os
from django.conf import settings

##페이지 별로 필요한 request를 컨트롤
#---------------분석도구 import ----------------

from rest_framework.decorators import api_view

@api_view(['GET'])
def main_page(request):
    user = loginValidator(request)
    return render(request,'src/Views/Main/main.html')

# @api_view(['GET'])
# def download_guide(request):
#     file_name = 'smartfarm_guidebook.pdf'
#     return attach_file(file_name, os.path.join(settings.MEDIA_ROOT, file_name))

