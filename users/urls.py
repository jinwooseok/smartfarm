from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/email/', views.validEmail, name='valid_email'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]