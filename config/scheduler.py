from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from ..smartfarm.models import Temp, LearnedModel
from django.utils import timezone
logger = logging.getLogger('django')

def temp_model_delete():
    delete_time = timezone.now()-timezone.timedelta(hours=1)
    Temp.objects.filter(created_at__lt=delete_time).delete()
    LearnedModel.objects.filter(created_at__lt=delete_time).delete()    
def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(
        temp_model_delete,
        trigger=CronTrigger(minute=0),
        id="delete",
        misfire_grace_time=300,
        replace_existing=True,
    )
    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()