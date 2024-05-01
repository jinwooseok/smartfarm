from django.db import models

# Create your models here.
def user_model_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/model/{1}'.format(instance.user.id, file_root)

class LearnedModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    original_file_name = models.CharField(max_length=200, default=None)
    model_name = models.CharField(max_length=200, default=None)
    model_root = models.CharField(max_length=200, default=None)
    model_meta_name = models.CharField(max_length=200, default=None)
    model_meta_root = models.CharField(max_length=200, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, model, model_meta : dict, *args, **kwargs):
        # joblib.dump를 사용하여 파일 저장
        self.model_root = self.get_model_file_path()
        self.model_meta_root = self.get_model_meta_file_path()
        with open(self.model_root, 'wb') as f:
            pickle.dump(model, f)
        with open(self.model_meta_root, 'w', encoding='utf-8') as f:
            json.dump(model_meta, f, ensure_ascii=False)
        super().save(*args, **kwargs)

    def get_model_file_path(self):
        # 파일이 저장될 경로 반환
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_name))
    
    def get_model_meta_file_path(self):
        # 파일이 저장될 경로 반환
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_meta_name))