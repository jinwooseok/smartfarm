from django.db import models

# Create your models here.
class FileFeature(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField(null=True)
    feature_selected = models.BooleanField(default=False)
    
class TempFeature(models.Model):
    temp = models.ForeignKey(Temp,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField(null=True)
    feature_selected = models.BooleanField(default=False)
    
class ModelFeature(models.Model):
    model = models.ForeignKey(LearnedModel,on_delete=models.CASCADE,default=000000)
    feature_name = models.CharField(max_length=200)
    feature_type = models.Choices('feature','target')
    weight = models.FloatField(null=True)