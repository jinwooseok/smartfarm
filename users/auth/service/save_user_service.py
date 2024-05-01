from users.auth.exceptions.auth_exceptions import EmailDuplicatedException, UserTelDuplicatedException
from argon2 import PasswordHasher
from users.models import User
from users.auth.repositorys import exist_user_by_email, exist_user_by_tel

class SaveUserService:
    def __init__(self, user_id, user_pw, user_name, user_job, user_tel):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_job = user_job
        self.user_tel = user_tel
    
    @classmethod
    def from_serializer(cls, serializer):
        user_id = serializer.validated_data['user_id']
        user_pw = serializer.validated_data['user_pw']
        user_name = serializer.validated_data['user_name']
        user_job = serializer.validated_data['user_job']
        user_tel = serializer.validated_data['user_tel']
        return cls(user_id, user_pw, user_name, user_job, user_tel)
    
    def execute(self):
        if self.is_duplicated_email(self.user_id):
            raise EmailDuplicatedException()
        #비밀번호 암호화
        self.user_pw = PasswordHasher().hash(self.user_pw)
        #전화번호 합체
        self.user_tel = ''.join(self.user_tel)
        #전화번호 검증
        if self.is_duplicated_user_tel(self.user_tel):
            raise UserTelDuplicatedException()
        #DB에 저장
        user_form = self.user_form()
        user_form.save()
    
    @staticmethod
    def is_duplicated_user_tel(user_tel):
        user_tel = ''.join(user_tel)
        return exist_user_by_tel(user_tel)
    
    @staticmethod
    def is_duplicated_email(email):
        return exist_user_by_email(email)
    
    def user_form(self):
        return User(user_id=self.user_id
                    , user_pw=self.user_pw
                    , user_name=self.user_name
                    , user_job=self.user_job
                    , user_tel=self.user_tel)