
from django.shortcuts import render

#-----------------------유틸리티 import-----------------------
##페이지 별로 필요한 request를 컨트롤
#---------------분석도구 import ----------------

from rest_framework.decorators import api_view
from django.http import HttpResponse
@api_view(['GET'])
def main_page(request):
    user_id = request.session.get('user')
    if user_id != None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.');location.href='/file-list/';</script>")
    return render(request,'src/Views/Main/main.html')
