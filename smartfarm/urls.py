from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from smartfarm import views

app_name='smartfarm'

urlpatterns = [
    #기타
    path('', views.main_page, name='main_page'),
    #path('download/guidebook/',views.download_guide, name='download_guide'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

