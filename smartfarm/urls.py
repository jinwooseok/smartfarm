from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='smartfarm'

urlpatterns = [
    path('',views.main, name = 'main'),
    #데이터관리 창
    path('manage/', views.manage, name='manage'),
    path('uploading/',views.file_uploading, name='uploading'),
    path('manage/delete/', views.fileDelete, name="fileDelete"),
    #merge 창
    path('merge/', views.merge, name='merge'),

    #데이터수정 창
    path('manage/show/<str:file_name>', views.show, name='show'),


    # path('CreateFile/',views.CreateFile, name="CreateFile"),
    path('excel/',views.excel, name='excel'),
    path('probing/', views.probing, name='probing'),
    path('excel/loaddata/',views.load_data,name='loaddata'),
    path('manage/show/farm/', views.farm, name='farm'),

    path('test/',views.test, name='test'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

