"""
DB에 삭제 신호가 오는 경우, 파일 시스템에 저장된 모델을 자동으로 삭제
"""
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from analytics.models import LearnedModel
from file.utils.utils import search_file_absolute_path
from file.utils.signals import delete_local_file
@receiver(pre_delete, sender=LearnedModel)
def delete_model(sender, instance, **kwargs):
    """
    설명
    - 모델이 삭제되기 전에 호출되는 함수.
    - DB에서 모델이 삭제되면 모델 파일을 삭제한다.
    - receiver 데코레이터를 사용하여 LearnedModel로부터 신호를 받는다. 모델이 삭제되기 전에 호출되도록 설정
    """
    delete_local_file(search_file_absolute_path(instance.model_root))
    delete_local_file(search_file_absolute_path(instance.model_meta_root))