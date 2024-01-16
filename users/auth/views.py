from django.shortcuts import render, redirect
from ..models import User
from argon2 import PasswordHasher, exceptions
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from rest_framework import exceptions
# Create your views here.
from rest_framework import viewsets
from .serializers import SignUpSerializer
class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    def page(self, request):
        if authenticate(request) is None:
            raise exceptions.NotAuthenticated()
        return render(request, 'src/Views/Register/register.html')
    
    def sign_up(self, request):
        user_id=request.POST['registerID']
        if self.is_duplicated_email(user_id):
            return HttpResponse("<script>alert('이미 존재하는 이메일입니다.');location.href='.';</script>")
        #비밀번호는 argon2의 hash함수를 사용해 db에 저장
        user_pw=request.POST['registerPassword']
        user_pw=PasswordHasher().hash(user_pw)
        
        user_name=request.POST['name']
        
        user_job=request.POST['registerJob']
        #phone에서 3개의 요소를 받기 때문에 (###,####,####) getlist로 값을 받음
        user_tel=request.POST.getlist('phone')
        user_tel = ''.join(user_tel)
        if User.objects.filter(user_tel=user_tel).exists():
            return HttpResponse("<script>alert('이미 존재하는 전화번호입니다.');location.href='.';</script>")
        user=User(
            user_id = user_id,
            user_pw = user_pw,
            user_name = user_name,
            user_tel = user_tel,
            user_job = user_job,
        )
        user.save()
        return redirect('users:login')
    
    def valid_email(self, request):
        register_id = request.POST.get('registerID')
        if self.is_duplicated_email(register_id):
            return JsonResponse({'data':True})
        return JsonResponse({'data':False})
        
    def is_duplicated_email(email):
        if User.objects.filter(user_id=email).exists():
            return True
        return False

class SignInViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    
    def page(self, request):
        return render(request, 'src/Views/Login/login.html')
    
    def sign_in(self, request):
        if request.session.get('user'):
            return redirect('/')

        login_user_id=request.POST['id']
        login_user_pw=request.POST['password']

        try:
            user = User.objects.get(user_id=login_user_id)
        except User.DoesNotExist:
            user=None
            context = {
                'error' : '계정이 존재하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        try :
            PasswordHasher().verify(user.user_pw.encode(), login_user_pw.encode())
        except exceptions.VerifyMismatchError:
            user=None  
            context = {
                'error' : '비밀번호가 일치하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        if user != None:
            request.session['user'] = user.id
        
            # Redirect to a success page.
            return redirect('/')
            
        else:
            context = {
                'error' : '로그인에 실패하였습니다.'
            }
            return render(request, 'Html/login.html', context)

class SignOutViewSet(viewsets.ModelViewSet):
        
    queryset = User.objects.all()

    def sign_out(self, request):
        request.session.flush()
        return redirect('/')
