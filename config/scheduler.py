"""
스케줄러를 모아놓은 파일
1시간마다 Temp와 LearnedModel을 삭제하는 스케줄러를 만들었다.

라이브러리
    BackgroundScheduler : 백그라운드에서 스케줄러를 실행할 수 있게 해주는 라이브러리
    CronTrigger : cron 표현식을 사용할 수 있게 해주는 라이브러리
    logging : 로깅을 위한 라이브러리
    Temp : Temp 모델
    LearnedModel : LearnedModel 모델
    timezone : 시간대를 사용하기 위한 라이브러리
"""
import logging
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from file.models import Temp
from analytics.models import LearnedModel

# settings.py의 LOGGER 변수에 django로 설정된 logger 객체를 호출함. - Django의 기본 로거
logger = logging.getLogger('django')

def temp_model_delete():
    """
    설명
        1시간 전에 생성된 Temp와 LearnedModel을 삭제하는 함수. 파일이 쌓이는 것을 방지하기 위한 스케줄러
    """
    delete_time = timezone.now()-timezone.timedelta(hours=1)
    Temp.objects.filter(created_at__lt=delete_time).delete()
    LearnedModel.objects.filter(created_at__lt=delete_time).delete()

def start():
    """
    설명
        스케줄러를 시작하는 함수. apps.py에 등록되어 앱 시작 시 사용된다.
        매시간 0분에 temp_model_delete 함수를 실행한다.
    """
    scheduler=BackgroundScheduler()
    scheduler.add_job(
        temp_model_delete,
        trigger=CronTrigger(minute=0),
        id="delete",
        misfire_grace_time=300,
        replace_existing=True,
    )
    try: #스케줄러 실행 시 발생하는 로그
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt: #스케줄러 종료 시 발생하는 로그로 키보드 개입이 있을 시 발생
        logger.info("Stopping scheduler...")
        scheduler.shutdown()