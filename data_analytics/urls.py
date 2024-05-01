from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

from .file.views import FileViewSet

app_name='smartfarm'


urlpatterns = [
     #분석
    path('analytics/<str:file_title>/',DataAnalyticsViewSet.as_view({'get':'page'})),
    path('analytics/<str:file_title>/model/',DataAnalyticsViewSet.as_view({'post':'create_model'})),
    path('analytics/<str:model_title>/model/download/',DataAnalyticsViewSet.as_view({'get':'download_model'})),\
    path('analytics/<str:model_title>/model/predict/',DataAnalyticsViewSet.as_view({'post':'predict'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)