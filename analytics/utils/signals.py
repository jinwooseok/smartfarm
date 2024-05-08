from django.db.models.signals import pre_delete
from django.dispatch import receiver
from analytics.models import LearnedModel
from file.utils.utils import search_file_absolute_path
from file.utils.signals import delete_local_file
@receiver(pre_delete, sender=LearnedModel)
def delete_model(sender, instance, **kwargs):
    delete_local_file(search_file_absolute_path(instance.model_root))
    delete_local_file(search_file_absolute_path(instance.model_meta_root))