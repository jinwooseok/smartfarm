from django.apps import AppConfig


class DataAnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_analytics'
    def ready(self):
        from .data_analytics.utils import signals
        from . import scheduler
        scheduler.start()