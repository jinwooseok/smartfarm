# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# import logging
# from .models import Temp, LearnedModel
# from django.utils import timezone
# logger = logging.getLogger(__name__)

# def temp_model_delete():
#     delete_time = timezone.now()-timezone.timedelta(days=1)
#     Temp.object.filter(created_at__lt=delete_time).delete()
#     LearnedModel.object.filter(created_at__lt=delete_time).delete()    
# def start():
#     scheduler=BackgroundScheduler()
#     scheduler.add_job(
#         temp_model_delete,
#         trigger=CronTrigger(hour=0, minute=0),
#         id="delete",
#         misfire_grace_time=300,
#         replace_existing=True,
#     )
#     try:
#         logger.info("Starting scheduler...")
#         scheduler.start()
#     except KeyboardInterrupt:
#         logger.info("Stopping scheduler...")
#         scheduler.shutdown()