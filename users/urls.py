from django.urls import path
from .auth.views import SignInViewSet, SignOutViewSet, SignUpViewSet

app_name='users'

urlpatterns = [
    path('sign-up/', SignUpViewSet.as_view({"get":"page","post":"sign_up"}), name='sign_up'),
    path('sign-up/email/', SignUpViewSet.as_view({"post":"valid_email"}), name='valid_email'),
    #sign-up/phone/send/
    #sign-up/phone/verify/
    path('sign-in/', SignInViewSet.as_view({"get":"page","post":"sign_in"}), name='sign_in'),
    path('sign-out/', SignOutViewSet.as_view({"post":"sign_out"}), name='sign_out'),
]