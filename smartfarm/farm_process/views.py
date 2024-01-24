from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from common.response import *
from rest_framework import exceptions

class DataABMSViewSet(viewsets.GenericViewSet):
    def page(self, request, file_title):
        return render(request, 'src/Views/ABMS/abms.html')
    
class FarmProcessViewSet(viewsets.GenericViewSet):
    

    def process_farm():
        return 0
    