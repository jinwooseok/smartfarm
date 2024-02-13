from django.db.models.signals import post_save
from django.dispatch import receiver
from ...models import LearnedModel
from ...feature.serializers import ModelFeatureSerializer
from ...feature.service.feature_service import FeatureService

@receiver(post_save, sender=LearnedModel)
def create_file(sender, instance, **kwargs):
    
    feature_info_list = FeatureService.extract_model_feature(instance)
    
    #변수 정보 저장
    feature_serializer = ModelFeatureSerializer(data=feature_info_list, many=True)
    feature_serializer = serializer_validator(feature_serializer)
    
    feature_serializer.save()