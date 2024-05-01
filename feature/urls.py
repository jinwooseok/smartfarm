from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

from .file.views import FileViewSet

app_name='smartfarm'


urlpatterns = [
    #파일 변수 호출
    path('files/<str:file_title>/data/feature/',FeatureViewSet.as_view({'get':'feature_list'})),
    path('files/<str:file_title>/data/feature/importance/',FeatureViewSet.as_view({'post':'create_feature_importance'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)