from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='smartfarm'

urlpatterns = [
    path('',views.main, name = 'main'),
    path('mypage/', views.mypage, name='mypage'),
    path('fileSave/',views.fileSave, name="filesave"),


    path('excel/',views.excel, name='excel'),
    path('probing/', views.probing, name='probing'),
    path('excel/loaddata/',views.load_data,name='loaddata'),
    path('uploading/',views.file_uploading, name='uploading'),
    path('excel/farm/', views.farm, name='farm'),

    path('test/',views.test, name='test'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

