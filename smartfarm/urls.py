from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

from .file.views import FileViewSet
from .file_data.views import FileDataViewSet, DataMergeViewSet
from .data_analytics.views import DataAnalyticsViewSet
from .farm_process.views import DataABMSViewSet, FarmProcessViewSet
app_name='smartfarm'


urlpatterns = [
    #기타
    path('', views.main_page, name='main_page'),
    #path('download/guidebook/',views.download_guide, name='download_guide'),

    #파일 관련
    path('file-list/',FileViewSet.as_view({'get':'page'})),
    path('files/',FileViewSet.as_view({'get':'list'})),
    path('files/file-name/',FileViewSet.as_view({'get':'name_list'})),
    path('files/save/',FileViewSet.as_view({'post':'save'})),
    path('files/delete/',FileViewSet.as_view({'delete':'delete'})),
    path('files/download/',FileViewSet.as_view({'post':'download'})),

    #파일 수정 페이지 호출
    path('revise/<str:file_title>/',FileDataViewSet.as_view({'get':'page'})),
    
    #파일 데이터 관련
    path('files/<str:file_title>/data/',FileDataViewSet.as_view({'get':'details'})),
    path('files/<str:file_title>/data/summary/',FileDataViewSet.as_view({'get':'summary'})),
    path('files/<str:file_title>/data/preprocess/',FileDataViewSet.as_view({'post':'process_outlier'})),
    path('files/<str:file_title>/data/timeseries/',FileDataViewSet.as_view({'post':'process_time_series'})),

    #농업 처리 도메인관련
    path('files/<str:file_title>/data/farm/',FarmProcessViewSet.as_view({'post':'process_farm'})),
    path('abms/<str:file_title>/',DataABMSViewSet.as_view({'get':'page'})),
    path('abms/<str:file_title>/env/',DataABMSViewSet.as_view({'get':'page'})),


    #분석
    path('analytics/<str:file_title>/',DataAnalyticsViewSet.as_view({'get':'page'})),
    #병합
    path('merge/',DataMergeViewSet.as_view({'get':'page','post':'merge'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

