from users.auth.exceptions.auth_exceptions import IdNotFoundException, PasswordNotMatchedException
from users.models import User
from argon2 import PasswordHasher
from users.auth.repositorys import get_user_by_email
from argon2.exceptions import VerifyMismatchError

class AuthUserService:
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
    
    @classmethod
    def from_serializer(cls, serializer):
        user_id = serializer.validated_data['email']
        user_pw = serializer.validated_data['password']
        return cls(user_id, user_pw)
    
    def execute(self):
        user = get_user_by_email(self.user_id)
        self.is_correct_password(user.user_pw, self.user_pw)
        return user
    
    @staticmethod
    def is_correct_password(user_pw,login_pw):
        try:
            return PasswordHasher().verify(user_pw, login_pw)
        except:    
            raise PasswordNotMatchedException()