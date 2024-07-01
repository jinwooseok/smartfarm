from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
@api_view(['GET'])
def main_page(request):
    user_id = request.session.get('user')
    if user_id is not None:
        return redirect('/file-list/')
    return render(request,'src/Views/Main/main.html')
