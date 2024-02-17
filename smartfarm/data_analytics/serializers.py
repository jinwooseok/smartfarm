from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..models import LearnedModel
from ..file.exceptions.file_exception import FileNotFoundException
class CreateModelSerializer(FileNameSerializer):
    modelName = serializers.CharField()
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    trainSize = serializers.FloatField()
    model = serializers.ChoiceField(choices=[("linear","linear"),("ridge","ridge"),("lasso","lasso"),("elastic","elastic"),("decision","decision"),("random","random"),("gradient","gradient"),("adaboost","adaboost"),("xgboost","xgboost"),("lightgbm","lightgbm"),("catboost","catboost")])

class ModelNameSerializer(serializers.Serializer):
    modelName = serializers.CharField()
    
    def get_model_object(self, user)->LearnedModel:
        try:
            return LearnedModel.objects.get(user=user, model_name=self.data['modelName'])
        except LearnedModel.DoesNotExist:
            raise FileNotFoundException()
        
class PredictModelSerializer(ModelNameSerializer):
    testData = serializers.JSONField()
    xValue = serializers.CharField()
    yValue = serializers.CharField()