from django.urls import path

import views
from django.conf import settings
from django.conf.urls.static import static
from file.views import FileViewSet

app_name='file'


urlpatterns = [
    path('file-list/',FileViewSet.as_view({'get':'page'})),
    path('files/',FileViewSet.as_view({'get':'list'})),
    path('files/file-name/',FileViewSet.as_view({'get':'name_list'})),
    path('files/save/',FileViewSet.as_view({'post':'save'})),
    path('files/delete/',FileViewSet.as_view({'delete':'delete'})),
    path('files/download/',FileViewSet.as_view({'post':'download'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)