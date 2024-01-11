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
    path('file-list/upload/',views.fileUploadApi, name='fileUpload'),
    path('file-list/delete/', views.fileDeleteApi, name="fileDelete"),
    
    #merge 창
    path('merge/', views.fileMergeView, name='merge'),
    path('merge-view/', views.fileMergeApi, name='mergeView'),
    #데이터수정 창
    path('revise/<str:file_title>/', views.dataEditView, name='revise'),
    path('revise/', views.dataEditWithNoFileView, name='revise2'),
    path('revise/<str:file_title>/preprocess/', views.preprocessorApi, name='preprocess'),
    path('revise/<str:file_title>/abms/growth/', views.abms_growth_api, name='abms_growth'),
    path('revise/<str:file_title>/abms/env/', views.abms_env_api, name='abms_env'),
    #farm
    path('loaddata/',views.dataLoadApi,name='loaddata'),
    path('revise/<str:file_title>/farm/', views.farm, name='farm'),
    #분석
    path('fileList_2/', views.fileList2, name='fileList2'),
    path('analyze/<str:file_title>/', views.getAnalyzeDataApi, name='getAnalyzeDataApi'),
    path("analyze/<str:file_title>/stat", views.useAnalizer, name='stat'),
    #a
    #util기능
    path('download/', views.fileDownloadApi, name='download'),
    path('scaler/', views.scalerApi, name='scaler'),
    path('download/guidebook/',views.guideBookDownloadApi, name='guidebook'),
    #test url 추가
    path('test/', views.test, name='test'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

