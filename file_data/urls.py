from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from file_data.views import FileDataViewSet, DataMergeViewSet

app_name='smartfarm'


urlpatterns = [
    #파일 수정 페이지 호출
    path('revise/<str:file_title>/',FileDataViewSet.as_view({'get':'page'})),
    #파일 데이터 관련
    path('files/<str:file_title>/data/',FileDataViewSet.as_view({'get':'details'})),
    path('files/<str:file_title>/data/summary/',FileDataViewSet.as_view({'get':'summary'})),
    path('files/<str:file_title>/data/preprocess/',FileDataViewSet.as_view({'post':'process_outlier'})),
    path('files/<str:file_title>/data/timeseries/',FileDataViewSet.as_view({'post':'process_time_series'})),
    #병합
    path('merge/',DataMergeViewSet.as_view({'get':'page','post':'merge'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)