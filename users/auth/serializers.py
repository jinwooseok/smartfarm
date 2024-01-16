from rest_framework import serializers
from ..models import User
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'user_pw', 'user_name', 'user_tel', 'user_job')