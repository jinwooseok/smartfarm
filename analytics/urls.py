"""
analytics app의 urls를 정의한다.
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from analytics.views import DataAnalyticsViewSet

app_name='analytics'

"""
urlpatterns는 URL 패턴을 정의하는 변수이다.
- analytics/<str:file_title>/ : 데이터 분석 페이지
- analytics/<str:file_title>/model/ : 모델 생성
- analytics/<str:model_title>/model/download/ : 모델 다운로드
- analytics/<str:model_title>/model/predict/ : 모델 예측 (미완성)
"""
urlpatterns = [
    #분석
    path('analytics/<str:file_title>/'
         ,DataAnalyticsViewSet.as_view({'get':'page'})),

    path('analytics/<str:file_title>/model/'
         ,DataAnalyticsViewSet.as_view({'post':'create_model'})),

    path('analytics/<str:model_title>/model/download/'
         ,DataAnalyticsViewSet.as_view({'get':'download_model'})),

    path('analytics/<str:model_title>/model/predict/'
         ,DataAnalyticsViewSet.as_view({'post':'predict'})),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
