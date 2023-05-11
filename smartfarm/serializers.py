from rest_framework import serializers
from .models import File_db
from users.models import User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_db
        fields = ['user_id', 'file_Title', 'file_Root', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name','user_id','user_pw']

    