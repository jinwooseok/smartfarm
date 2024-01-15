from rest_framework import viewsets
from django.shortcuts import render
from ..models import File
#데이터 관련 뷰셋
class FileDataViewSet(viewsets.ModelViewSet):

    queryset = File.objects.all()

    # def page(self, request):
    #     return render(request, 'src/Views/')

    def details():
        return 0
    def summary():
        return 0
    def process_outlier():
        return 0
    def process_farm():
        return 0
    def process_time_series():
        return 0