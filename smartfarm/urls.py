from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='smartfarm'

urlpatterns = [
    #데이터관리 창
    path('', views.main, name='main'),
    path('data_list/', views.data_list, name='data_list'),
    path('data_list/upload/',views.fileUploadView, name='upload'),
    path('data_list/delete/', views.fileDeleteView, name="fileDelete"),
    #merge 창
    path('merge/', views.merge, name='merge'),

    #데이터수정 창
    path('revise/<str:file_name>/', views.revise, name='revise'),
    path('revise/', views.revise2, name='revise2'),

    #path('probing/', views.probing, name='probing'),
    path('revise/loaddata/',views.fileLoadView,name='loaddata'),
    path('revise/farm/', views.farm, name='farm'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

