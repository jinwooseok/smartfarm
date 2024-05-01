from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from farm_process.views import FarmProcessViewSet, DataABMSViewSet

app_name='farm_process'


urlpatterns = [
    #농업 처리 도메인관련
    path('files/<str:file_title>/data/farm/',FarmProcessViewSet.as_view({'post':'process_farm'})),
    path('abms/<str:file_title>/',DataABMSViewSet.as_view({'get':'page'})),
    path('abms/<str:file_title>/env/',DataABMSViewSet.as_view({'post':'process_abms'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)