"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [ #하위 폴더들의 모든 URL들과 연결시켜주는 역할
    path('admin/', admin.site.urls),
    path('',include('smartfarm.urls')),
    path('',include('file.urls')),
    path('',include('feature.urls')),
    path('',include('farm_process.urls')),
    path('',include('file_data.urls')),
    path('',include('analytics.urls')),
    path('users/',include('users.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
