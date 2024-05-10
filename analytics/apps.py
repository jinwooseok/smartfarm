from django.apps import AppConfig

class AnalyticsConfig(AppConfig):
    """
    AnalyticsConfig 클래스는 앱의 설정을 정의하는 클래스입니다.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'
    def ready(self):
        """
        - ready 메서드는 앱이 실행될 때 호출되는 메서드입니다. 서버 실행 시 호출됨.
        - signals 모듈을 import하여 모델 삭제 전에 파일을 삭제하도록 합니다.
        - scheduler를 import하여 실행합니다.
        """
        from analytics.utils import signals
        from config import scheduler
        scheduler.start()