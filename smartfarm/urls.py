from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='smartfarm'


urlpatterns = [
    #데이터관리 창
    path('', views.main, name='main'),
    #화면 연결
    path('file-list/', views.fileListView, name='fileList'),
    #api
    path('file-list/upload/',views.fileUpload, name='fileUpload'),
    path('file-list/delete/', views.fileDelete, name="fileDelete"),
    
    #merge 창
    path('merge/', views.merge, name='merge'),
    path('merge-view/', views.mergeView, name='mergeView'),
    #데이터수정 창
    path('revise/<str:file_name>/', views.revise, name='revise'),
    path('revise/', views.revise2, name='revise2'),
    path('revise/<str:file_name>/preprocess/', views.usePreprocessor, name='preprocess'),

    #farm
    path('loaddata/',views.fileLoadView,name='loaddata'),
    path('revise/<str:file_name>/farm/', views.farm, name='farm'),
    #분석
    path('fileList_2/', views.fileList2, name='fileList2'),
    path('analyze/<str:file_name>/', views.analyze, name='analysisView'),
    path("analyze/<str:file_name>/stat", views.useAnalizer, name='stat'),
    
    #util기능
    path('download/', views.fileDownloadView, name='download'),
    #api
    path('api/users/', views.userApiView),
    path('api/files/', views.fileListApiView),

    #test url 추가
    path('test/', views.test, name='test'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

