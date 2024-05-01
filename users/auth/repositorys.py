from users.models import User
from exceptions.auth_exceptions import IdNotFoundException
def exist_user_by_email(email):
    return User.objects.filter(user_id=email).exists()

def exist_user_by_tel(tel):
    return User.objects.filter(user_tel=tel).exists()

def get_user_by_email(email):
    try:
        return User.objects.get(user_id=email)
    except User.DoesNotExist:
        raise IdNotFoundException()